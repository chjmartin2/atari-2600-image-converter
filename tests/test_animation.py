import unittest
import numpy as np
from chrono.animation import FrameClock,persistence_frames
from chrono.core import frame_pixels,Settings,hardware_palette

class AnimationTests(unittest.TestCase):
    def test_frame_order_and_delayed_callback(self):
        clock=FrameClock(100,60)
        self.assertEqual([clock.number(100+i/60)%3 for i in range(6)],[0,1,2,0,1,2])
        self.assertEqual(clock.number(101),60) # one-second stall must not slow phase

    def test_pause_resume_speed_change_and_step(self):
        clock=FrameClock(0,60);clock.toggle(.025)
        self.assertEqual(clock.number(10),1)
        clock.step(10);self.assertFalse(clock.running);self.assertEqual(clock.number(20),2)
        clock.set_rate(10,20);clock.toggle(21)
        self.assertEqual(clock.number(21.2),4)
        clock.set_rate(3,21.2)
        self.assertEqual(clock.number(22.2),7)

    def test_raw_mode_preserves_component_frames(self):
        indices=np.random.default_rng(3).integers(0,8,(128,48),dtype=np.uint8)
        frames=frame_pixels(indices,Settings().codes)
        np.testing.assert_array_equal(persistence_frames(frames,0),frames)
        self.assertFalse(np.array_equal(frames[0],hardware_palette(Settings().codes)[indices]))

    def test_persistence_trails_previous_phase_without_changing_average(self):
        frames=np.zeros((3,128,48,3),dtype=np.uint8);frames[0,:,:,0]=210
        out=persistence_frames(frames,.5)
        self.assertEqual(list(out[:,0,0,0]),[120,60,30])
        np.testing.assert_array_equal(out.mean(axis=0),frames.mean(axis=0))
        with self.assertRaises(ValueError):persistence_frames(frames,1)

if __name__=='__main__':unittest.main()
