"""声音审核已按用户要求取消；旧命令仅作兼容，不伪称听审。"""
import argparse,json,hashlib,subprocess,sys,wave
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'_references'))
from voice_review_policy import review_not_required
VOICE_SHA='2fdc74cefd85628ed6c95f93b905857816289f530cfccc1cda2622f5f8cf4fd8'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def duration(path):
 r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)],capture_output=True,text=True,check=True)
 return float(json.loads(r.stdout)['format']['duration'])
def validate(path=None,video_sha256=None,stage='delivery'):
 return review_not_required('voice_cadence')
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('report',type=Path,nargs='?');parser.add_argument('--stage',choices=['voice_ready','delivery'],default='delivery');parser.add_argument('--video-sha256');parser.add_argument('--output',type=Path);args=parser.parse_args();result=validate(args.report,args.video_sha256,args.stage)
 if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
