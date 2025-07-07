# List of Taipy controls

This table shows a list of Taipy controllers, with links to the official documentation:

| Control Name                                                                                         | value          | lov           | on_action | on_change                                 |
| ---------------------------------------------------------------------------------------------------- | -------------- | ------------- | --------- | ----------------------------------------- |
| [text](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/text/)                   | Yes            | No            | No        | No                                        |
| [button](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/button/)               | No             | No            | Yes       | No                                        |
| [input](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/input/)                 | Yes            | No            | Yes       | Yes                                       |
| [number](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/number/)               | Yes            | No            | Yes       | Yes                                       |
| [slider](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/slider/)               | Yes            | Yes           | No        | Yes                                       |
| [toggle](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/toggle/)               | Yes            | Yes           | No        | No                                        |
| [date](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/date/)                   | Yes* (date)    | No            | No        | Yes                                       |
| [date_range](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/date_range/)       | Yes* (dates)   | No            | No        | Yes                                       |
| [chart](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/chart/)                 | Yes* (data)    | No            | No        | Yes**(on_change  <br>and on_range_change) |
| [table](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/table/)                 | Yes* (data)    | Yes (columns) | No        | Yes *** (several)                         |
| [file_selector](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/file_selector/) | No             | No            | Yes       | No                                        |
| [file_download](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/file_download/) | No             | No            | Yes       | No                                        |
| [Image](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/image/)                 | Yes* (content) | No            | Yes       | No                                        |
| [indicator](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/indicator/)         | Yes            | No            | No        | No                                        |
| [selector](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/selector/)           | Yes            | Yes           | No        | Yes                                       |
| [status](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/status/)               | Yes            | No            | No        | No                                        |
| [tree](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/tree/)                   | Yes            | Yes           | No        | Yes                                       |
| [chat](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/chat/)                   | Yes*(messages) | No            | Yes       | No                                        |
| [metric](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/metric/)               | Yes            | No            | No        | No                                        |
| [indicator](https://docs.taipy.io/en/release-4.1/refmans/gui/viselements/generic/metric/)            | Yes            | No            | No        | No                                        |

\* The value parameter exists but isn't called that. 

** Charts include lots of sub-types, and you have 2 types of on_change Callbacks.

*** Tables have 3 different Callbacks that happen at row or cell level.
