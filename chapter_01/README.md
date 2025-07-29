# Chapter 1

- [Chapter 1](#chapter-1)
  - [Hello Worlds](#hello-worlds)
  - [Installing development version](#installing-development-version)
  - [Taipy CLI](#taipy-cli)

## Hello Worlds

Chapter 1 shows how to create some "Hello World" apps for different components of Taipy. The directory `hello_worlds` has the code for all the "apps".

![Screenshot of a header in a Taipy app](./img/hello_earth.png)

The directory `my_first_app_from_cli` shows the skeleton of a ultiple-page app:

![image of a multiple page app (tabs)](./img/multi_pages.png)

## Installing development version

The book focuses on installing stables versions. You can also install the development version, even if it's not stable (you may want to contribute to the library or get a feature that is not available in the latest stable release). Most of the time, this is not recommended.
You can retrieve it from GitHub using git:

```bashgit clone git://github.com/avaiga/taipy
```

Then, from the folder, install it with pip:

```bash
pip install .
```

## Taipy CLI

The chapter also covers Taipy's CLI tool. [You can check the official documentation](https://docs.taipy.io/en/latest/manuals/cli/).

The directories `my_first_app_from_cli` and `my_first_scenatrion_from_cli` are 2 Taipy applications structures that come out straight out of `taipy create`.

Taipy CLI creates a `requirements.txt` file, but it doesn't specify the version, we recommend adding it as well (for example change `taipy` with `taipy==4.1.0` or whatever version you are running). Since this is a minimal example, we left the outcome as is.
