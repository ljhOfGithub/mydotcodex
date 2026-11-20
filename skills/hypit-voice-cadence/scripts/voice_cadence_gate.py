"""核验原片节奏、本人连续配音、真实确认及最终PCM；不冒充听检。"""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path
import subprocess
import wave

VOICE_SHA = '2fdc74cefd85628ed6c95f93b905857816289f530cfccc1cda2622f5f8cf4fd8'

def need(ok, message):
    if not ok: raise ValueError(message)

def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()

def spoken_text(text):
    # 仅忽略分句空白；不删除标点、表演提示或任何口播字符。
    return re.sub(r'\s+', '', text)

def wav(path):
    with wave.open(str(path), 'rb') as stream:
        return stream.getparams(), stream.readframes(stream.getnframes())

def duration(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    return float(json.loads(result.stdout)['format']['duration'])

def validate(path, video_sha256=None, stage='delivery'):
    path = Path(path)
    report = json.loads(path.read_text())
    def bind(item):
        file = path.parent / item['path']
        need(file.is_file() and file.stat().st_size > 0 and sha(file) == item['sha256'], '证据文件缺失或哈希变化：'+str(file))
        return file
    need(stage in ('voice_ready', 'delivery'), '未知检查阶段')
    need(report.get('format') == 'hypit-reference-voice@1', '缺少新版原片节奏配音证据')
    reference_video = bind(report['reference_video'])
    voice_reference = bind(report['voice_reference'])
    need(sha(voice_reference) == VOICE_SHA and report.get('model') == 'VoxCPM2', '须沿用已验证的本人VoxCPM2声源')
    script = bind(report['script'])
    sentences = [x.strip() for x in script.read_text().splitlines() if x.strip()]
    need(bool(sentences), '确认口播稿为空')
    audio = bind(report['full_audio'])
    params, pcm = wav(audio)
    need(params.framerate == 48000 and params.sampwidth == 2 and params.nchannels in (1, 2), '完整试听须为48kHz PCM16，声道为单声道或双声道')
    source_duration = duration(reference_video)
    output_duration = params.nframes / params.framerate
    segments = report['segments']
    need([x['id'] for x in segments] == list(range(1, len(sentences)+1)), '原片和改写稿须逐句完整对应')
    previous_source = previous_output = 0.0
    for item, text in zip(segments, sentences):
        need(item['text'] == text, '节奏表与确认稿不一致')
        a,b = item['source_window']; c,d = item['output_window']
        need(all(isinstance(v,(float,int)) and not isinstance(v,bool) and math.isfinite(v) for v in (a,b,c,d)), '节奏时码必须为有限数值')
        need(previous_source <= a < b <= source_duration+.04 and previous_output <= c < d <= output_duration+.001, '逐句时窗重叠、倒序或越界')
        need(bool(item.get('rhythm_notes','').strip()), '逐句须记录停顿、重音或节奏差异，不只填总时长')
        previous_source, previous_output = b,d
    opening_count = min(3,len(sentences))
    source_opening = segments[opening_count-1]['source_window'][1]-segments[0]['source_window'][0]
    output_opening = segments[opening_count-1]['output_window'][1]-segments[0]['output_window'][0]
    drift = abs(output_duration/source_duration-1)
    opening_drift = abs(output_opening/source_opening-1)
    if max(drift,opening_drift) > .10:
        need('duration_exception' in report, '节奏偏离原片超过10%，须重配或绑定用户明确改长/改短的依据')
        exception = json.loads(bind(report['duration_exception']).read_text())
        need(exception.get('source') == 'actual_user_reply' and exception.get('duration_change_explicitly_approved') is True and bool(exception.get('exact_quote','').strip()), '节奏偏离原片超过10%，须重配或绑定用户明确改长/改短的依据')
    need(report.get('reference_audio_used_as_voice_reference') is False, '原片只能参照节奏，不能偷换成原作者声线')
    opening = bind(report['opening_audio'])
    groups = report['generation_groups']
    covered = []
    need(bool(groups) and groups[0]['mode']=='opening' and groups[0]['sentence_ids'] == list(range(1,opening_count+1)), '开头前三句须先连续生成，不得拼接三个互不相干的试配')
    need(groups[0]['audio']['sha256'] == sha(opening), '开头上下文不是本轮选定的本人声音')
    for index, group in enumerate(groups):
        ids = group['sentence_ids']; covered.extend(ids)
        need(ids and ids == list(range(ids[0],ids[-1]+1)) and all(1 <= i <= len(sentences) for i in ids), '生成语义段编号无效')
        target = ''.join(sentences[i-1] for i in ids)
        need(spoken_text(group['target_text']) == spoken_text(target) and group['model']=='VoxCPM2' and group['voice_reference_sha256']==sha(voice_reference), '生成文本、模型或本人声源失配')
        raw = bind(group['audio']); bind(group['generation_evidence'])
        need(group.get('tempo_rate')==1 and group.get('pitch_shift_semitones')==0 and group.get('gain')==1 and group.get('formant_shift') is False, '节奏必须在生成时形成，禁止后期拉伸、移调或改增益')
        if index:
            need(group['mode']=='continuation' and bind(group['context_audio'])==opening and spoken_text(group['context_text'])==spoken_text(groups[0]['target_text']), '后文须沿用本轮开头的本人声音和对应文本续接')
            need(spoken_text(group['api_text'])==spoken_text(target), '续接text只能是纯口播；禁止把表演指令拼到前面或混入正文')
        asr = json.loads(bind(group['independent_asr']).read_text())
        need(asr.get('audio_sha256')==sha(raw) and bool(asr.get('recognized','').strip()) and asr.get('content_verified') is True, '必须另做独立转写核对内容，不能拿强制对齐证明没有多读文字')
        for token in ('延续前文','表演指令','抬高后收住','不额外重读'):
            need(token in target or token not in asr['recognized'], '实际声音读出了表演提示：'+token)
    need(covered==list(range(1,len(sentences)+1)), '语义段漏句、重句或顺序改变')
    approval = json.loads(bind(report['full_audio_approval']).read_text())
    need(approval.get('source')=='actual_user_reply' and approval.get('audio_sha256')==sha(audio) and approval.get('entire_audio_listened') is True and bool(approval.get('exact_quote','').strip()), '必须先给用户完整音轨试听并保存真实认可，不能只交前三句')
    quote=approval['exact_quote']
    need(any(word in quote for word in ('可以保留','按原速保留','接受','认可','通过','满意')) and not any(word in quote for word in ('不够激动','还是像人机','还有一句需要调整','还有问题','不可以','不接受','不认可','不通过','不满意')), '模糊改善或用户指出的问题不能当成认可')
    result={'status':'VOICE_READY','audio_sha256':sha(audio),'sentences':len(sentences),'generation_groups':len(groups),'source_duration':source_duration,'output_duration':output_duration,'duration_deviation':drift,'opening_duration_deviation':opening_drift,'tempo_rate':1.0,'scope':'材料、实际时长及生成链核验；不代替真实听检，不宣称逐音节复制。'}
    if stage=='delivery':
        video=bind(report['actual_video'])
        need(video_sha256 is None or sha(video)==video_sha256, '配音门绑定的不是当前MP4')
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=sample_rate,channels','-of','json',str(video)]))['streams'][0]
        need(int(probe['sample_rate'])==params.framerate and probe['channels'] in (params.nchannels,2), '配回成片时改变了采样率或声道')
        actual=subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(video),'-map','0:a:0','-c:a','pcm_s16le','-f','s16le','-'],capture_output=True,check=True).stdout
        mapping='unchanged'
        if params.nchannels==1 and probe['channels']==2:
            from array import array
            channels=array('h');channels.frombytes(actual)
            need(channels[::2]==channels[1::2], '复制单声道后左右采样不同')
            actual=channels[::2].tobytes();mapping='mono_to_identical_dual_mono'
        need(len(actual)>=len(pcm) and actual[:len(pcm)]==pcm and not any(actual[len(pcm):]), '最终成片声音与获批整轨不再逐采样相同，须恢复原音；有损相似度不能替代')
        result.update(status='PASS',video_sha256=sha(video),bit_exact_approved_pcm=True,channel_mapping=mapping)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report',type=Path);parser.add_argument('--stage',choices=['voice_ready','delivery'],default='delivery');parser.add_argument('--video-sha256');parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try: result=validate(args.report,args.video_sha256,args.stage)
    except (ValueError,KeyError,TypeError,OSError,subprocess.SubprocessError,wave.Error) as error: result={'status':'FAIL','reason':str(error)}
    if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False));return int(result['status']=='FAIL')

if __name__=='__main__':raise SystemExit(main())
