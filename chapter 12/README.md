# Chapter 12: Improving the performance of Taipy applications

This chapter has several mini-apps that demonstrate each Chapter's concept. Here are the the directories:

* `state`: see how to optimize the use of `State` in your Callbacks.
* `long_callbacks`: using long running Callbacks in Taipy.
* `threads`: Setting `threading` manually in Taipy appliations.
* `hold_and_resume`: How to "block" your UI while tasks execute in the back.
* `partials`: how to use Partials with Taipy.
* `job_execution_mode`: How to use asynchronous executions with the Taipy Orchestrator.
* `exercices`: Code with the answers to the Chapter's questions.

This chapter doesn't use external data, we retrieve data from some URLs using `requests` but we don't process it further (we use it as an example to test `threading`).