from doxygenlogparser.log_parser import validate_args
from doxygenlogparser.log_parser import LogParser
import unittest
from argparse import Namespace
from unittest.mock import patch, MagicMock, mock_open

class TestValidateArgs(unittest.TestCase):
    @patch('doxygenlogparser.log_parser.os.path.exists')
    def test_valid_args(self, mock_exists):
        mock_exists.return_value = True
        args = Namespace(warning_log_file='warning_log.txt', output='out.csv')
        return_val = validate_args(args)
        self.assertEqual(return_val.warning_log_file, 'warning_log.txt')
        self.assertEqual(return_val.output, 'out.csv')

    @patch('doxygenlogparser.log_parser.os.path.exists')
    def test_warning_log_file_does_not_exist(self, mock_exists):
        mock_exists.return_value = False
        args = Namespace(warning_log_file='warning_log.txt', output='out.csv')

        with self.assertRaises(ValueError) as ctx:
            validate_args(args)
        self.assertEqual(str(ctx.exception), 'warning_log_file "warning_log.txt" does not exist!')

    @patch('doxygenlogparser.log_parser.os.path.exists')
    def test_set_default_output_file(self, mock_exists):
        mock_exists.return_value = True
        args = Namespace(warning_log_file='warning_log.txt', output=None)
        return_val = validate_args(args)
        self.assertEqual(return_val.warning_log_file, 'warning_log.txt')
        self.assertEqual(return_val.output, 'output.csv')


class TestLogParser(unittest.TestCase):
    def test_generate_csv_with_standard_warning_lines(self):
        test_data = (
            "/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/core/xds/xds_client/xds_client.h:234: warning: Found ';' while parsing initializer list! (doxygen could be confused by a macro call without semicolon)\n"
            "/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/php/tests/qps/generated_code/GPBMetadata/Src/Proto/Grpc/Testing/Messages.php:7: warning: Compound GPBMetadata::Src::Proto::Grpc::Testing::Messages is not documented.\n"
        )
        expected_csv_rows = [
            ["/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/core/xds/xds_client/xds_client.h", "234",
             "warning: Found ';' while parsing initializer list! (doxygen could be confused by a macro call without semicolon)"],
            [
                "/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/php/tests/qps/generated_code/GPBMetadata/Src/Proto/Grpc/Testing/Messages.php",
                "7", "warning: Compound GPBMetadata::Src::Proto::Grpc::Testing::Messages is not documented."]
        ]
        log_parser = LogParser('warning_file.txt', 'output.csv')
        mock_input_file = mock_open(read_data=test_data)
        mock_csv_writer = MagicMock()
        with patch("builtins.open", mock_input_file), patch('doxygenlogparser.log_parser.csv.writer', return_value=mock_csv_writer):
            log_parser.parse_file()

        mock_csv_writer.writerow.assert_called_once_with(["file", "line", "message"])
        mock_csv_writer.writerows.assert_called_once_with(expected_csv_rows)

    def test_generate_csv_with_non_standard_warning_lines(self):
        test_data = (
            "/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/core/xds/xds_client/xds_client.h:234: warning: Found ';' while parsing initializer list! (doxygen could be confused by a macro call without semicolon)\n"
            "/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/php/tests/qps/generated_code/GPBMetadata/Src/Proto/Grpc/Testing/Messages.php:7: warning: Compound GPBMetadata::Src::Proto::Grpc::Testing::Messages is not documented.\n"
            "/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/cpp/ext/gcp/observability.cc:253: warning: no uniquely matching class member found for GcpObservability & grpc::GcpObservability::operator=(GcpObservability &&other)\n"
            "Possible candidates:\n"
            "  'Reader & grpc_core::RequestBuffer::Reader::operator=(const Reader &)=delete' at line 46 of file /var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/core/call/request_buffer.h\n"
            "  'SubchannelKey & grpc_core::SubchannelKey::operator=(const SubchannelKey &other)=default' at line 44 of file /var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/core/client_channel/subchannel_pool_interface.h\n"
            "  'SubchannelKey & grpc_core::SubchannelKey::operator=(SubchannelKey &&other) noexcept=default' at line 46 of file /var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/core/client_channel/subchannel_pool_interface.h\n"
        )
        expected_csv_rows = [
            ["/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/core/xds/xds_client/xds_client.h", "234",
             "warning: Found ';' while parsing initializer list! (doxygen could be confused by a macro call without semicolon)"],
            [
                "/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/php/tests/qps/generated_code/GPBMetadata/Src/Proto/Grpc/Testing/Messages.php",
                "7", "warning: Compound GPBMetadata::Src::Proto::Grpc::Testing::Messages is not documented."],
            ["/var/jenkins_home/workspace/Test_01/repoA/doxygenLogParser/cpp/ext/gcp/observability.cc", "253",
             "warning: no uniquely matching class member found for GcpObservability & grpc::GcpObservability::operator=(GcpObservability &&other)"]
        ]
        log_parser = LogParser('warning_file.txt', 'output.csv')
        mock_input_file = mock_open(read_data=test_data)
        mock_csv_writer = MagicMock()
        with patch("builtins.open", mock_input_file), patch('doxygenlogparser.log_parser.csv.writer', return_value=mock_csv_writer):
            log_parser.parse_file()

        mock_csv_writer.writerow.assert_called_once_with(["file", "line", "message"])
        mock_csv_writer.writerows.assert_called_once_with(expected_csv_rows)


if __name__ == '__main__':
    unittest.main()