"""合成夹具回归，不作为真实配音或用户认可证据。"""
from copy import deepcopy
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import wave
import voice_cadence_gate as gate

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        def audio(name,frames):
            path=self.root/name
            with wave.open(str(path),'wb') as stream:
                stream.setparams((1,2,48000,frames,'NONE','not compressed'));stream.writeframes(struct.pack('<h',1000)*frames)
            return path
        self.audio=audio
        self.full=audio('full.wav',48000);self.opening=audio('opening.wav',14400);self.body=audio('body.wav',33600);self.voice=audio('voice.wav',4800)
        self.addCleanup(patch.stopall);patch.object(gate,'VOICE_SHA',gate.sha(self.voice)).start()
        self.script=self.root/'script.txt';self.script.write_text('第一句！\n第二句！\n第三句！\n后文。\n')
        self.video=self.root/'video.mp4'
        subprocess.run(['ffmpeg','-nostdin','-v','error','-f','lavfi','-i','color=s=64x64:r=30:d=1','-i',str(self.full),'-c:v','libx264','-c:a','flac','-strict','experimental',str(self.video)],check=True)
        def obj(name,data):
            path=self.root/name;path.write_text(json.dumps(data,ensure_ascii=False));return self.bound(path)
        self.obj=obj
        ack=obj('approval.json',{'test_fixture':True,'source':'actual_user_reply','audio_sha256':gate.sha(self.full),'entire_audio_listened':True,'exact_quote':'合成夹具：完整听完，激动有起伏，按原速保留。'})
        groups=[]
        for ids,raw,mode,text in [([1,2,3],self.opening,'opening','第一句！第二句！第三句！'),([4],self.body,'continuation','后文。')]:
            groups.append({'mode':mode,'sentence_ids':ids,'audio':self.bound(raw),'model':'VoxCPM2','voice_reference_sha256':gate.sha(self.voice),'target_text':text,'api_text':text,'generation_evidence':obj(mode+'-request.json',{'test_fixture':True}),
                'tempo_rate':1.0,'pitch_shift_semitones':0,'gain':1.0,'formant_shift':False,
                'independent_asr':obj(mode+'-asr.json',{'test_fixture':True,'audio_sha256':gate.sha(raw),'recognized':text,'content_verified':True})})
        groups[1].update(context_audio=self.bound(self.opening),context_text=groups[0]['target_text'])
        self.report={'format':'hypit-reference-voice@1','reference_video':self.bound(self.video),'voice_reference':self.bound(self.voice),'model':'VoxCPM2','script':self.bound(self.script),'full_audio':self.bound(self.full),'opening_audio':self.bound(self.opening),'actual_video':self.bound(self.video),'reference_audio_used_as_voice_reference':False,'full_audio_approval':ack,'generation_groups':groups,
            'segments':[{'id':i,'text':t,'source_window':[a,b],'output_window':[a,b],'rhythm_notes':'合成夹具：保留句间停顿，记录实际范围。'} for i,t,a,b in [(1,'第一句！',0,.1),(2,'第二句！',.1,.2),(3,'第三句！',.2,.3),(4,'后文。',.3,1)]]}
    def bound(self,path):return {'path':str(path),'sha256':gate.sha(path)}
    def run_gate(self,stage='delivery'):
        path=self.root/'report.json';path.write_text(json.dumps(self.report,ensure_ascii=False));return gate.validate(path,stage=stage)
    def test_sentence_spacing_preserves_same_spoken_text(self):
        self.report['generation_groups'][0]['target_text']='第一句！ 第二句！ 第三句！'
        self.report['generation_groups'][1]['context_text']='第一句！ 第二句！ 第三句！'
        self.assertEqual(self.run_gate()['status'],'PASS')
    def test_whitespace_does_not_erase_direction_or_content(self):
        self.report['generation_groups'][1]['api_text']=' 延续前文 后文。'
        with self.assertRaises(ValueError):self.run_gate()
    def test_context_extra_word_rejected_with_spaces(self):
        self.report['generation_groups'][1]['context_text']='第一句！ 第二句！ 错词 第三句！'
        with self.assertRaises(ValueError):self.run_gate()
    def test_valid_full_chain(self):self.assertTrue(self.run_gate()['bit_exact_approved_pcm'])
    def test_before_render_does_not_require_video(self):
        self.report.pop('actual_video');self.assertEqual(self.run_gate('voice_ready')['status'],'VOICE_READY')
    def test_46_second_drift_is_rejected(self):
        self.full=self.audio('long.wav',67200);self.report['full_audio']=self.bound(self.full)
        with self.assertRaises((ValueError,KeyError)):self.run_gate()
    def test_unapproved_opening_drift(self):
        self.report['segments'][2]['output_window'][1]=.36;self.report['segments'][3]['output_window'][0]=.36
        with self.assertRaises((ValueError,KeyError)):self.run_gate()
    def test_later_reference_window_drift_still_needs_notes(self):
        self.report['segments'][3]['rhythm_notes']=''
        with self.assertRaises(ValueError):self.run_gate()
    def test_continuation_cannot_read_direction(self):
        self.report['generation_groups'][1]['api_text']='(延续前文兴奋地讲解)后文。'
        with self.assertRaises(ValueError):self.run_gate()
    def test_independent_asr_catches_spoken_direction(self):
        self.report['generation_groups'][1]['independent_asr']=self.obj('bad-asr.json',{'audio_sha256':gate.sha(self.body),'recognized':'延续前文，后文。','content_verified':True})
        with self.assertRaises(ValueError):self.run_gate()
    def test_source_voice_not_author_voice(self):
        self.report['reference_audio_used_as_voice_reference']=True
        with self.assertRaises(ValueError):self.run_gate()
    def test_context_must_be_same_own_opening(self):
        self.report['generation_groups'][1]['context_audio']=self.bound(self.body)
        with self.assertRaises(ValueError):self.run_gate()
    def test_context_text_matches_audio(self):
        self.report['generation_groups'][1]['context_text']='别的开头'
        with self.assertRaises(ValueError):self.run_gate()
    def test_first_three_not_separate_generation(self):
        self.report['generation_groups'][0]['sentence_ids']=[1]
        with self.assertRaises(ValueError):self.run_gate()
    def test_missing_sentence(self):
        self.report['segments'].pop()
        with self.assertRaises(ValueError):self.run_gate()
    def test_no_asr_is_not_replaced_by_alignment(self):
        self.report['generation_groups'][1]['independent_asr']=self.obj('alignment.json',{'items':[]})
        with self.assertRaises(ValueError):self.run_gate()
    def test_no_speed_or_pitch_postprocessing(self):
        for field,value in [('tempo_rate',1.01),('pitch_shift_semitones',1),('gain',1.01),('formant_shift',True)]:
            report=deepcopy(self.report);self.report['generation_groups'][1][field]=value
            with self.assertRaises(ValueError):self.run_gate()
            self.report=report
    def test_historical_approval_wrong_audio(self):
        self.report['full_audio_approval']=self.obj('wrong-ack.json',{'source':'actual_user_reply','audio_sha256':gate.sha(self.body),'entire_audio_listened':True,'exact_quote':'可以保留'})
        with self.assertRaises(ValueError):self.run_gate()
    def test_negative_feedback_not_acceptance(self):
        self.report['full_audio_approval']=self.obj('negative.json',{'source':'actual_user_reply','audio_sha256':gate.sha(self.full),'entire_audio_listened':True,'exact_quote':'不够激动，还是像人机'})
        with self.assertRaises(ValueError):self.run_gate()
    def test_improvement_does_not_mean_approval(self):
        self.report['full_audio_approval']=self.obj('improvement.json',{'source':'actual_user_reply','audio_sha256':gate.sha(self.full),'entire_audio_listened':True,'exact_quote':'感觉好多了，你怎么做的'})
        with self.assertRaises(ValueError):self.run_gate()
    def test_explicit_duration_change_can_be_bound(self):
        self.report['segments'][2]['output_window'][1]=.36;self.report['segments'][3]['output_window'][0]=.36
        self.report['duration_exception']=self.obj('duration-approval.json',{'source':'actual_user_reply','duration_change_explicitly_approved':True,'exact_quote':'合成夹具：允许片头加长到0.36秒。'})
        self.assertEqual(self.run_gate()['status'],'PASS')
    def test_changed_approved_pcm_is_rejected(self):
        changed=self.audio('changed.wav',48000)
        with wave.open(str(changed),'wb') as stream:stream.setparams((1,2,48000,48000,'NONE','not compressed'));stream.writeframes(struct.pack('<h',2000)*48000)
        self.report['full_audio']=self.bound(changed)
        self.report['full_audio_approval']=self.obj('changed-ack.json',{'source':'actual_user_reply','audio_sha256':gate.sha(changed),'entire_audio_listened':True,'exact_quote':'合成夹具认可'})
        with self.assertRaises(ValueError):self.run_gate()
    def test_stale_hash(self):
        self.script.write_text('改了内容')
        with self.assertRaises(ValueError):self.run_gate()

if __name__=='__main__':unittest.main(verbosity=2)
