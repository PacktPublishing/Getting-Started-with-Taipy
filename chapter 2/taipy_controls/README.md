# List of Taipy controls

This table shows a list of Taipy controllers, with links to the official documentation:

| Control Name                                                                            | value          | lov           | on_action | on_change                                   |
| --------------------------------------------------------------------------------------- | -------------- | ------------- | --------- | ------------------------------------------- |
| [text](https://docs.taipy.io/en/latest/manuals/gui/viselements/text/)                   | Yes            | No            | No        | No                                          |
| [button](https://docs.taipy.io/en/latest/manuals/gui/viselements/button/)               | No             | No            | Yes       | No                                          |
| [input](https://docs.taipy.io/en/latest/manuals/gui/viselements/input/)                 | Yes            | No            | Yes       | Yes                                         |
| [number](https://docs.taipy.io/en/latest/manuals/gui/viselements/number/)               | Yes            | No            | Yes       | Yes                                         |
| [slider](https://docs.taipy.io/en/latest/manuals/gui/viselements/slider/)               | Yes            | Yes           | No        | Yes                                         |
| [toggle](https://docs.taipy.io/en/latest/manuals/gui/viselements/toggle/)               | Yes            | Yes           | No        | No                                          |
| [date](https://docs.taipy.io/en/latest/manuals/gui/viselements/date/)                   | Yes* (date)    | No            | No        | Yes                                         |
| [date_range](https://docs.taipy.io/en/latest/manuals/gui/viselements/date_range/)       | Yes* (dates)   | No            | No        | Yes                                         |
| [chart](https://docs.taipy.io/en/latest/manuals/gui/viselements/chart/)                 | Yes* (data)    | No            | No        | Yes**(on_change<br><br>and on_range_change) |
| [table](https://docs.taipy.io/en/latest/manuals/gui/viselements/table/)                 | Yes* (data)    | Yes (columns) | No        | Yes *** (several)                           |
| [file_selector](https://docs.taipy.io/en/latest/manuals/gui/viselements/file_selector/) | No             | No            | Yes       | No                                          |
| [file_download](https://docs.taipy.io/en/latest/manuals/gui/viselements/file_download/) | No             | No            | Yes       | No                                          |
| [Image](https://docs.taipy.io/en/latest/manuals/gui/viselements/image/)                 | Yes* (content) | No            | Yes       | No                                          |
| [indicator](https://docs.taipy.io/en/latest/manuals/gui/viselements/indicator/)         | Yes            | No            | No        | No                                          |
| [selector](https://docs.taipy.io/en/latest/manuals/gui/viselements/selector/)           | Yes            | Yes           | No        | Yes                                         |
| [status](https://docs.taipy.io/en/latest/manuals/gui/viselements/status/)               | Yes            | No            | No        | No                                          |
| [tree](https://docs.taipy.io/en/latest/manuals/gui/viselements/tree/)                   | Yes            | Yes           | No        | Yes                                         |


\* The value parameter exists but isn't called that. 

** Charts include lots of sub-types, and you have 2 types of on_change Callbacks.

*** Tables have 3 different Callbacks that happen at row or cell level.
