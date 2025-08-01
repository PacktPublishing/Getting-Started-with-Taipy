# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
from pages import *
from taipy.gui import Gui

pages = {"/": root_page, "Page_1": Page_1, "Page_2": Page_2}


if __name__ == "__main__":

    gui = Gui(pages=pages)
    gui.run(title="My First Taipy App from the CLI")
