import unittest,math,wave,tempfile,subprocess,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from voice_review_policy import review_not_required,basic_audio
class PolicyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(tempfile.mkdtemp(prefix='voice-policy-regression-'))
  for name,amp in [('source.wav',8000),('changed.wav',4000)]:
   values=b''.join(int(amp*math.sin(2*math.pi*440*n/48000)).to_bytes(2,'little',signed=True)for n in range(4800))
   with wave.open(str(cls.root/name),'wb')as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes(values)
  subprocess.run(['ffmpeg','-nostdin','-v','error','-f','lavfi','-i','color=s=64x64:r=10:d=0.2','-an','-c:v','libx264','-pix_fmt','yuv420p',str(cls.root/'silent.mp4')],check=True)
 def test_review_is_disabled_not_fabricated(self):
  r=review_not_required();self.assertEqual(r['status'],'VOICE_REVIEW_NOT_REQUIRED');self.assertFalse(r['user_approval_required']);self.assertFalse(r['audit_performed']);self.assertNotIn('actual_listening',r)
 def test_real_wav_is_decodable(self):
  r=basic_audio(self.root/'source.wav');self.assertEqual(r['status'],'BASIC_AUDIO_OK');self.assertEqual(r['sample_rate'],48000)
 def test_missing_file_fails(self):
  with self.assertRaises(ValueError):basic_audio(self.root/'missing.wav')
 def test_missing_audio_fails(self):
  with self.assertRaises(ValueError):basic_audio(self.root/'silent.mp4')
 def test_original_pcm_remains_checked(self):
  self.assertTrue(basic_audio(self.root/'source.wav',source_audio=self.root/'source.wav')['original_rate_pcm_exact'])
 def test_changed_pcm_still_fails(self):
  with self.assertRaises(ValueError):basic_audio(self.root/'changed.wav',source_audio=self.root/'source.wav')
 def test_same_samples_at_changed_rate_fail(self):
  with wave.open(str(self.root/'source.wav'),'rb')as f:values=f.readframes(f.getnframes())
  with wave.open(str(self.root/'wrong-rate.wav'),'wb')as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000);f.writeframes(values)
  with self.assertRaises(ValueError):basic_audio(self.root/'wrong-rate.wav',source_audio=self.root/'source.wav')
if __name__=='__main__':unittest.main()
