# Chapter 11: Improving the performance of Taipy applications

- [Chapter 11: Improving the performance of Taipy applications](#chapter-11-improving-the-performance-of-taipy-applications)
  - [Repo Structure](#repo-structure)

## Repo Structure

This chapter has mini-apps that show each section's concept. Here are the directories:

- `state`: How to optimize the use of `State` in your Callbacks.
- `long_callbacks`: How to use long running Callbacks in Taipy.
- `threads`: How to set `threading` manually in Taipy applications.
- `hold_and_resume`: How to "block" your UI while tasks execute in the back.
- `partials`: How to use Partials with Taipy.
- `job_execution_mode`: How to use asynchronous executions with the Taipy Orchestrator.
- `exercices`: Code with the answers to the Chapter's questions.

This chapter doesn't use external data, we retrieve data from some URLs using `requests` but we don't process it further (we use it as an example to test `threading`).
