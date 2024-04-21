import unittest
import numpy as np
from ExtractorModules.mdd_extractor import MddExtractor
from data_extractor import DataExtractor


class TestMddExtractor(unittest.TestCase):
    def setUp(self):
        self.slice_count = 3
        self.slice_size = 5
        self.parameters_per_slice = 2
        self.slice_overlap = 1
        self.time_step = self.create_data_extractor([]).get_minimal_time_step() - 1

        self.line_up_data = [float(i) for i in range(1, 101)]
        self.line_down_data = [float(i) for i in range(100, 0, -1)]
        self.line_down_with_spikes_data = [self.line_down_data[i] for i in range(len(self.line_down_data))]
        for i in range(2, len(self.line_down_with_spikes_data), self.slice_size - self.slice_overlap):
            self.line_down_with_spikes_data[i] += 2
        self.random_data = [12.0, 16.0, 20.0, 24.0, 29.0, 33.0, 36.0, 36.0, 35.0, 34.0, 36.0, 40.0, 45.0, 50.0, 55.0,
                            59.0, 60.0, 57.0, 53.0, 48.0, 44.0, 43.0, 44.0, 45.0, 48.0, 51.0, 53.0, 54.0, 55.0, 57.0,
                            57.0, 58.0, 59.0, 60.0, 61.0, 61.0, 60.0, 58.0, 55.0, 52.0, 47.0, 42.0, 38.0, 36.0, 38.0,
                            42.0, 45.0, 49.0, 52.0, 55.0, 59.0, 63.0, 67.0, 70.0, 72.0, 73.0, 73.0, 71.0, 69.0, 69.0,
                            68.0, 67.0, 66.0, 64.0, 59.0, 55.0, 50.0, 48.0, 48.0, 48.0, 47.0, 47.0, 48.0, 49.0, 50.0,
                            48.0, 44.0, 41.0, 40.0, 40.0, 41.0, 44.0, 45.0, 47.0, 47.0, 46.0, 44.0, 42.0, 41.0, 39.0,
                            39.0, 41.0, 44.0, 45.0, 46.0, 47.0, 50.0, 54.0, 59.0, 63.0]

    def create_data_extractor(self, data):
        return DataExtractor(data, self.slice_count, self.slice_size, self.parameters_per_slice, self.slice_overlap)

    def create_mdd_extractor(self, data):
        return MddExtractor(self.create_data_extractor(data))

    def check_maximum_drawdowns(self, mdds, mdd_extractor):
        self.assertIsInstance(mdds, np.ndarray)
        self.assertEqual(mdds.shape[0], mdd_extractor.main_extractor.slice_count)

    def test_maximum_drawdown(self):
        mdd_extractor = self.create_mdd_extractor(self.line_up_data)
        mdds = mdd_extractor.get_maximum_drawdowns(self.time_step)
        self.check_maximum_drawdowns(mdds, mdd_extractor)
        for mdd in mdds:
            self.assertAlmostEqual(mdd, 0.)

        mdd_extractor = self.create_mdd_extractor(self.line_down_data)
        mdds = mdd_extractor.get_maximum_drawdowns(self.time_step)
        self.check_maximum_drawdowns(mdds, mdd_extractor)
        for i, mdd in enumerate(mdds):
            idx = i * (mdd_extractor.main_extractor.slice_size - mdd_extractor.main_extractor.slice_overlap)
            down = self.line_down_data[self.time_step - idx]
            peak = self.line_down_data[self.time_step - idx - mdd_extractor.main_extractor.slice_size + 1]
            self.assertAlmostEqual(mdds[i], (peak - down) / peak, msg=f"Slice: {i}, Peak: {peak}, Down: {down}")

        mdd_extractor = self.create_mdd_extractor(self.line_down_with_spikes_data)
        mdds = mdd_extractor.get_maximum_drawdowns(self.time_step)
        self.check_maximum_drawdowns(mdds, mdd_extractor)
        for i, mdd in enumerate(mdds):
            idx = i * (mdd_extractor.main_extractor.slice_size - mdd_extractor.main_extractor.slice_overlap)
            down = self.line_down_with_spikes_data[self.time_step - idx]
            peak = self.line_down_with_spikes_data[self.time_step - idx - mdd_extractor.main_extractor.slice_size + 3]
            self.assertAlmostEqual(mdds[i], (peak - down) / peak, msg=f"Slice: {i}, Peak: {peak}, Down: {down}")

        mdd_extractor = self.create_mdd_extractor(self.random_data)
        mdds = mdd_extractor.get_maximum_drawdowns(self.time_step)
        self.check_maximum_drawdowns(mdds, mdd_extractor)
        downs = [34., 35., 12.]
        peaks = [35., 36., 12.]
        for i, mdd in enumerate(mdds):
            self.assertAlmostEqual(mdds[i], (peaks[i] - downs[i]) / peaks[i],
                                   msg=f"Slice: {i}, Peak: {peaks[i]}, Down: {downs[i]}")

        mdds = mdd_extractor.get_maximum_drawdowns(self.time_step + 15)
        self.check_maximum_drawdowns(mdds, mdd_extractor)
        downs = [45., 43., 48.]
        peaks = [45., 48., 60.]
        for i, mdd in enumerate(mdds):
            self.assertAlmostEqual(mdds[i], (peaks[i] - downs[i]) / peaks[i],
                                   msg=f"Slice: {i}, Peak: {peaks[i]}, Down: {downs[i]}")


if __name__ == '__main__':
    unittest.main()
