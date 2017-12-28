import mock
import os

from mercury_agent.common.helpers.cli import CLIResult
from mercury_agent.hardware.raid.interfaces.megaraid import storcli

from ..base import MercuryAgentUnitTest


class StorcliTest(MercuryAgentUnitTest):
    @mock.patch('mercury.hardware.raid.interfaces.megaraid.storcli.cli')
    def test_run(self, mock_cli):
        mock_cli.run.return_value = CLIResult('', '', 0)
        mock_cli.find_in_path.return_value = '/sbin/storcli64'
        s = storcli.Storcli()
        assert s.run('') == ''

        mock_cli.run.return_value = CLIResult('Error', '', 1)

        self.assertRaises(storcli.StorcliException, s.run, *('', ))

    @mock.patch('mercury.hardware.raid.interfaces.megaraid.storcli.cli')
    def test_run_json(self, mock_cli):
        with open(os.path.join(os.path.dirname(__file__),
                               '../resources/storcli.json')) as fp:
            json_data = fp.read()

        mock_cli.run.return_value = CLIResult(json_data, '', 0)
        mock_cli.find_in_path.return_value = '/sbin/storcli64'
        s = storcli.Storcli()
        assert isinstance(s.run_json('/call show all'), dict)

        mock_cli.run.return_value = CLIResult('not_valid_json', '', 0)

        self.assertRaises(storcli.StorcliException, s.run_json, *('', ))

    @mock.patch('mercury.hardware.raid.interfaces.megaraid.storcli.cli')
    def test_controllers(self, mock_cli):
        with open(os.path.join(os.path.dirname(__file__),
                               '../resources/storcli.json')) as fp:
            json_data = fp.read()

        mock_cli.run.return_value = CLIResult(json_data, '', 0)
        mock_cli.find_in_path.return_value = '/sbin/storcli64'
        s = storcli.Storcli()
        assert isinstance(s.controllers, list)

        mock_cli.run.return_value = CLIResult('{}', '', 0)

        def _wrapper():
            return s.controllers

        self.assertRaises(storcli.StorcliException, _wrapper)

    @mock.patch('mercury.hardware.raid.interfaces.megaraid.storcli.cli')
    def test_delete(self, mock_cli):
        mock_cli.run.return_value = CLIResult('', '', 0)
        mock_cli.find_in_path.return_value = '/sbin/storcli64'
        s = storcli.Storcli()
        assert s.delete(0) == ''

    @mock.patch('mercury.hardware.raid.interfaces.megaraid.storcli.cli')
    def test_add(self, mock_cli):
        mock_cli.run.return_value = CLIResult('', '', 0)
        mock_cli.find_in_path.return_value = '/sbin/storcli64'

        s = storcli.Storcli()
        assert s.add(0, 'r0', '32:0-1') == ''
        assert s.add(0, 'r10', '32:0-3', pdperarray=2) == ''

        self.assertRaises(storcli.StorcliException, s.add, *(0, 'r10', '32:0-3'))

        with open(os.path.join(os.path.dirname(__file__), '../resources/storcli_err.txt')) as fp:
            error_data = fp.read()

        mock_cli.run.return_value = CLIResult(error_data, '', 0)

        self.assertRaises(storcli.StorcliException, s.add, *(0, '', ''))
