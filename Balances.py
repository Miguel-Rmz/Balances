#!Python
"""
Custom script for calculating balances from different financial
institutions and logging results in defined log file
"""

__author__ = 'mramirez'

import sys
# adding Utilities holding directory to PYTHONPATH
sys.path.append(r'C:\Scripts\Python')

import math, os, shutil
import argparse
import Utilities.Common_Utils as CU
from datetime import datetime

# cfg parameters
_LOGFILE = ''
_ARCHIVE = ''
_CHASELIMIT = 7700.00
_EXTRADEBT = 0.00

# uses default log location %userprofile%\Reports\Balances if _LOGFILE is null
# and default archive location %userprofile%\Reports\_Archive\Balances if _ARCHIVE is null
if not _LOGFILE:
    _LOGFILE = CU.create_logDirs(os.path.join(os.environ['userprofile'], 'Reports/Balances'), True, '%Y-%m-%d', 'Balances.log')

if not _ARCHIVE:
    _ARCHIVE = CU.create_logDirs(os.path.join(os.environ['userprofile'], 'Reports/_Archive/Balances'), True, '%Y-%m-%d_%H%M', 'Balances.log')

# argparse cmd parameters
parser = argparse.ArgumentParser()
parser.add_argument("Wells", help="Wells Fargo Available Balance", type=float)                                              # Required Wells AvailBal arg
parser.add_argument("Chase", help="Chase Credit Available Balance", type=float)                                             # Required Chase AvailBal arg
parser.add_argument('-d', '--debt', help='Extra Debt (Wells Credit, Payments, etc.)', type=float, default=0.00, nargs='*')  # Optional Pending Debt arg
parser.add_argument('-c', '--cash', help='Cash', type=float, default=0.00)                                                  # Optional Extra Cash arg
parser.add_argument('-s', '--spreadsheet', help='Spreadsheet', type=float, default=0.00)                                    # Optional Spreadsheet total arg
args = parser.parse_args()

# logs start of calculations
CU.logger_datetime(_LOGFILE, 'STARTING Balances Calculation')

# money calculations
chaseDebt, extraDebt = _CHASELIMIT - args.Chase, sum(args.debt)                                                             # Calculates chase and any extra debt
balance = round(args.Wells, 2) - round(chaseDebt, 2) - round(extraDebt, 2) + round(args.cash, 2)                            # Calculates final balance
spreadsheetDiff = abs(round(args.spreadsheet, 2) - balance)                                                                 # Calculates spreadsheet difference absolute value

# logs results
CU.logger_datetime(_LOGFILE, 'Parameters: [Wells]: {0:.2f}, [Chase]: {1:.2f}, [Extra Debt]: {2:.2f}, [Cash]: {3:.2f}, [Spreadsheet]: {4:.2f}'.format(round(args.Wells, 2), round(args.Chase, 2), round(extraDebt, 2), round(args.cash, 2), round(args.spreadsheet, 2)))
CU.logger_empty_line(_LOGFILE, '\tSummary:\n\t' + '-' * 42 + '\n')
CU.logger(_LOGFILE, '\tWells AvailBal:       {:.2f}'.format(round(args.Wells, 2)))
CU.logger(_LOGFILE, '\tChase Debt:         - {:.2f}'.format(round(chaseDebt, 2)))
CU.logger(_LOGFILE, '\tExtra Debt:         - {:.2f}'.format(round(extraDebt, 2)))
CU.logger(_LOGFILE, '\tExtra Cash:         + {:.2f}'.format(round(args.cash, 2)))
CU.logger(_LOGFILE, '\t                     ------------')
CU.logger(_LOGFILE, '\tActual Total:         {:.2f}'.format(balance))
CU.logger_empty_line(_LOGFILE, '\tSpreadsheet Diff:     {:.2f}\n\n'.format(spreadsheetDiff))
CU.logger_datetime(_LOGFILE, 'FINISHING Balances Calculation\n\n')

# renaming log and moving to _Archive location when spreadsheet_diff = 0.00
if '{:.2f}'.format(spreadsheetDiff) == '0.00':
    shutil.move(_LOGFILE, _ARCHIVE)
