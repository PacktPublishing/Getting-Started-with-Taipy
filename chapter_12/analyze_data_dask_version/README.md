# Analyze Data using Dask, and not Spark

We decided to create an alternative version of the `analyze_data` application, that uses Dask for the pre-processing, instead of Spark.

## Why this App?

As we mention in the book's chapter, the goal here is to show how to use different frameworks for large data with Taipy. In a real application, you'd likely stick to one single option, instead of increasing the complexity of your app, like we did in our showcase example.

The downside of this approach is that, **since some users may find it too challenging to install Spark, and since this app requires both Spark and Dask, users who can install Dask can't benefit from the book's examples.**

**We created this application replacing the pre-processing with Spark with a preprocessing with Dask, this way, everyone should be able to run it.**

> **IMPORTANT Remarks**:
>
> 1. You may find it challenging to install Spark, we still recommend you don't give up! You can do it, maybe try again tomorrow!
> 2. You may have installed Spark and made the book's example work: Congrats! Now you can also run the Dask version!

## Extra Requirements

You'll need to install Dask Distributed:

```bash
pip install dask[distributed]
```

We didn't include it in the `requirements.txt`.

## Main Differences

This app uses a function that leverages Dask as a Python library, directly, we place it in `process_nyc_tlc.py`. Obviously, the code is different, since we use another library, but we also need one file, instead of two for the Spark version (because we chose to run it as a CLI program).
