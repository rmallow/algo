# Changelog
All notable changes to this project will be documented in this file.

## [0.6.0] - 2021-06-22
### Added
- mpLogging for better logging across multiple processes and to stream it to logging window
- Logging window along with logging model for handling mpLogging updates from the mainframe
- Logging queue in mainframe for getting logging updates
- Status window for monitoring status of currently running blocks
- Status model for receiving updates from mainframe for statuses
- Mainframe now queries blocks for information/status and also tracks the time of the queries
- This change log for major releases

### Fixed
- Fixed issue with feed table not correctly updating on period for UI

### Changed
- Mainframe start loop is now running off of threading timers
- Moved qt .ui classes to their own subdirectory as ui folder was getting crowded
- Converted current logging over to mpLogging

## [0.5.0] - 2021-05-15
### Added
- Connected main model to output view
- Connected output select to main model
- Enabled tracking of data between mainframe and block
- Used queues to transfer information from block -> UI
- Created pandas model for displaying pandas data

### Fixed
- Eliminated type error caused by faulty get data's
- Added env variables to fix weird mac issues with threading and url requests
- Updated labeling to be correct for output view

### Changed
- Added details to command processor
- Added details to messages
- Moved animations to a seperate util file

## [0.4.0] = 2021-04-01
### Added
- Began tracking progress on Trello and for future work (work before this was not tracked and therefore will not be in changelog)
- Create dataFunc class for getting data off a user supplied function
- Reddit func example using data funcs
- Added keyword unpacker helper class
- Feed can now use automatic unique identifiers if needed
- Added required words for keyword unpacker
- Major refactoring of UI to have a more output focus
- Added output select screens to determine what output is wanted to track

## Fixed
- Fixed issues with multiple inheritance caused by keywordUnpacker and commandProcessor by adding multiBase
- Refactored event for non-sequentail indexing
- Handled issue when there are duplicate values sent to feed
- updating command processor to be slightly more generic

## Changed
- Moved QT stuff out of mainframe/start and into ui so it would not be needed at all on server
- Move commandProcessor to commonUtil
- Removed "async" from handler and handler manager names
- Cleaned up handlerManager loading to use **dict
- Refactored action class for keywordUnpacker
- Removed "m_" from fields, this was because I was use to it in C++, but is not needed at all for python
