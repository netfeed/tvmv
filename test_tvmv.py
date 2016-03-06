import imp
import os
import os.path
import unittest

tvmv = imp.load_source('tvmv', 'tvmv')
tvmv.VERBOSE = False

episodes = [
    "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4",
    "files/American.Dad.S01E08.HDTV.x264/American Dad - 1x08.mp4",
    "files/American.Dad.S01E07.HDTV.x264/107.mp4",
    "files/American.Dad.S11E08.HDTV.x264/American Dad - 1108.mp4",
    "files/American.Dad.S11E09.HDTV.x264/American.Dad.S11E09.HDTV.x264.mp4",
    "files/Bobs.Burgers.S05E15.HDTV.x264.mp4",
    "files/It's Always Sunny in Philadelphia S10E10 (1920x1080).mkv",
]

class TestSeasonParsing(unittest.TestCase):
    def test_s01e08(self):
        result = tvmv.parse_season("American.Dad.S01E08.HDTV.x264")
        self.assertEqual('01', result.group(1))
        self.assertEqual('08', result.group(2))

    def test_07e09(self):
        result = tvmv.parse_season("Cutthroat+Kitchen+07e09+hdtv+x264")
        self.assertEqual('07', result.group(1))
        self.assertEqual('09', result.group(2))

    def test_s11e23(self):
        result = tvmv.parse_season("American.Dad.S11E23.HDTV.x264")
        self.assertEqual('11', result.group(1))
        self.assertEqual('23', result.group(2))

    def test_parent(self):
        result = tvmv.parse_season("American.Dad.S11E23.HDTV.x264/episode.mp4")
        self.assertEqual('11', result.group(1))
        self.assertEqual('23', result.group(2))

    def test_1x10(self):
        result = tvmv.parse_season("American Dad 1x10  HDTV x264")
        self.assertEqual('1', result.group(1))
        self.assertEqual('10', result.group(2))

    def test_10x01(self):
        result = tvmv.parse_season("American Dad 10x01  HDTV x264")
        self.assertEqual('10', result.group(1))
        self.assertEqual('01', result.group(2))

    def test_110(self):
        result = tvmv.parse_season("American Dad 110  HDTV x264")
        self.assertEqual('1', result.group(1))
        self.assertEqual('10', result.group(2))

    def test_1001(self):
        result = tvmv.parse_season("American Dad 1001  HDTV x264")
        self.assertEqual('10', result.group(1))
        self.assertEqual('01', result.group(2))

    def test_none(self):
        result = tvmv.parse_season("American Dad HDTV x264")
        self.assertEqual(None, result)

    def test_slash_season(self):
        result = tvmv.parse_season("511 - Mac and Charlie Write a Movie.avi")
        self.assertEqual('5', result.group(1))
        self.assertEqual('11', result.group(2))

    def test_number_in_ep(self):
        result = tvmv.parse_season("205 - 100 Dollar Baby.avi")
        self.assertEqual('2', result.group(1))
        self.assertEqual('05', result.group(2))


class TestNameParsing(unittest.TestCase):
    def test_s01e08(self):
        result = tvmv.parse_name("American.Dad.S01E08.HDTV.x264")
        self.assertEqual('American Dad', result)

    def test_1x10(self):
        result = tvmv.parse_name("American Dad 1x10  HDTV x264")
        self.assertEqual('American Dad', result)

    def test_110(self):
        result = tvmv.parse_name("American Dad 110  HDTV x264")
        self.assertEqual('American Dad', result)

    def test_sunny(self):
        result = tvmv.parse_name("It's Always Sunny in Philadelphia 1001  HDTV x264")
        self.assertEqual("It's Always Sunny in Philadelphia", result)

    def test_none(self):
        result = tvmv.parse_name("American Dad HDTV x264")
        self.assertEqual(None, result)

    def test_archer(self):
        result = tvmv.parse_name("Archer.2009.S06E11.HDTV.x264")
        self.assertEqual("Archer 2009", result)

class TestTvParsing(unittest.TestCase):
    def test_name_single_number_season(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        check = tvmv.Show('American Dad', episode=tvmv.Episode(1, 8, '.mp4'))
        self.assertEqual(check, parsed)

    def test_name_single_number_season_x(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 1x08.mp4")
        check = tvmv.Show('American Dad', episode=tvmv.Episode(1, 8, '.mp4'))
        self.assertEqual(check, parsed)

    def test_check_dir(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E07.HDTV.x264/107.mp4")
        check = tvmv.Show('American Dad', episode=tvmv.Episode(1, 7, '.mp4'))
        self.assertEqual(check, parsed)

    def test_check_dir_no_files(self):
        parsed = tvmv.parse_path('files', "American.Dad.S01E07.HDTV.x264/107.mp4")
        check = tvmv.Show('American Dad', episode=tvmv.Episode(1, 7, '.mp4'))
        self.assertEqual(check, parsed)

    def test_name_double_digit_season(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S11E08.HDTV.x264/American Dad - 1108.mp4")
        check = tvmv.Show('American Dad', episode=tvmv.Episode(11, 8, '.mp4'))
        self.assertEqual(check, parsed)

    def test_am_good_filename(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S11E09.HDTV.x264/American.Dad.S11E09.HDTV.x264.mp4")
        check = tvmv.Show('American Dad', episode=tvmv.Episode(11, 9, '.mp4'))
        self.assertEqual(check, parsed)

    def test_bb_good_filename(self):
        parsed = tvmv.parse_path('files', "files/Bobs.Burgers.S05E15.HDTV.x264.mp4")
        check = tvmv.Show('Bobs Burgers', episode=tvmv.Episode(5, 15, '.mp4'))
        self.assertEqual(check, parsed)

    def test_spaced_name(self):
        parsed = tvmv.parse_path('files', "files/It's Always Sunny in Philadelphia S10E10 (1920x1080).mkv")
        check = tvmv.Show("It's Always Sunny in Philadelphia", episode=tvmv.Episode(10, 10, '.mkv'))
        self.assertEqual(check, parsed)

    def test_spaced_name_no_files(self):
        parsed = tvmv.parse_path('files', "It's Always Sunny in Philadelphia S10E10 (1920x1080).mkv")
        check = tvmv.Show("It's Always Sunny in Philadelphia", episode=tvmv.Episode(10, 10, '.mkv'))
        self.assertEqual(check, parsed)

    def test_one_up(self):
        parsed = tvmv.parse_path('files', "It's Always Sunny In Philadelphia/Season 3/309 - Sweet Dee's Dating A Retarted Person.avi")
        check = tvmv.Show("It's Always Sunny In Philadelphia", episode=tvmv.Episode(3, 9, '.avi'))
        self.assertEqual(check, parsed)

    def test_one_up_none(self):
        parsed = tvmv.parse_path('files', "files/Season 3/309 - Sweet Dee's Dating A Retarted Person.avi")
        self.assertEqual(None, parsed)

    def test_number_in_name(self):
        parsed = tvmv.parse_path('files', "files/It's Always Sunny In Philadelphia/Season 2/205 - 100 Dollar Baby.avi")
        check = tvmv.Show("It's Always Sunny In Philadelphia", episode=tvmv.Episode(2, 5, '.avi'))
        self.assertEqual(check, parsed)

class TestFormatFromPath(unittest.TestCase):
    def test_name(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        result = parsed.format("{show}/{show}")
        self.assertEqual("American Dad/American Dad", result)

    def test_season(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        result = parsed.format("{season}")
        self.assertEqual("1", result)

    def test_padded_season(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        result = parsed.format("{season.pad(2)}")
        self.assertEqual("01", result)

    def test_episode(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        result = parsed.format("{episode}")
        self.assertEqual("8", result)

    def test_padded_episode(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        result = parsed.format("{episode.pad(2)}")
        self.assertEqual("08", result)

    def test_1x8_combo(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        result = parsed.format("{season}x{episode}")
        self.assertEqual("1x8", result)

    def test_padded_combo(self):
        parsed = tvmv.parse_path('files', "files/American.Dad.S01E08.HDTV.x264/American Dad - 108.mp4")
        result = parsed.format("s{season.pad(2)}e{episode.pad(2)}")
        self.assertEqual("s01e08", result)

if __name__ == '__main__':
    unittest.main()
