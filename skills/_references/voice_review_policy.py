"""2026-11-26：用户取消声音审核；仅提供音轨文件与原速完整性检查。"""
from pathlib import Path
import hashlib,json,subprocess
POLICY_ID='voice-review-not-required-20261126'
def review_not_required(component='voice'):
 return {'status':'VOICE_REVIEW_NOT_REQUIRED','policy':POLICY_ID,'component':component,'review_required':False,'user_approval_required':False,'audit_performed':False,'reason':'用户明确要求以后声音不再审核；不要求试听、A/B、情绪、音质或逐句批准。'}
def basic_audio(path,*,source_audio=None):
 path=Path(path)
 if not path.is_file():raise ValueError('音轨载体文件不存在')
 r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True)
 if r.returncode:raise ValueError('音轨载体无法读取')
 d=json.loads(r.stdout);a=next((s for s in d['streams']if s['codec_type']=='audio'),None)
 if a is None or int(a.get('sample_rate',0))<=0:raise ValueError('缺少可用音轨')
 r=subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(path),'-map','0:a:0','-f','null','-'],capture_output=True,text=True)
 if r.returncode:raise ValueError('音轨无法完整解码')
 result={**review_not_required('basic_file_integrity'),'status':'BASIC_AUDIO_OK','path':str(path.resolve()),'sample_rate':int(a['sample_rate']),'channels':int(a['channels']),'decode_exit':0}
 if source_audio is not None:
  def pcm(f):
   q=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(f),'-map','0:a:0','-f','s16le','-c:a','pcm_s16le','-'],capture_output=True)
   if q.returncode:raise ValueError('原速音轨无法解码')
   return q.stdout
  source_probe=subprocess.run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=sample_rate,channels','-of','json',str(source_audio)],capture_output=True,text=True,check=True)
  source_stream=json.loads(source_probe.stdout)['streams'][0]
  if int(source_stream['sample_rate'])!=int(a['sample_rate']) or int(source_stream['channels'])!=int(a['channels']):raise ValueError('指定原音的采样率或声道改变')
  source=pcm(Path(source_audio));actual=pcm(path)
  if not actual.startswith(source)or any(actual[len(source):]):raise ValueError('指定原速音轨样本改变或非静音补尾')
  result['original_rate_pcm_exact']=True;result['source_pcm_sha256']=hashlib.sha256(source).hexdigest()
 return result
