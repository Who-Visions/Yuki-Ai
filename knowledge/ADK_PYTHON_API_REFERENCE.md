# ADK Python API Reference

## google.adk.a2a module
## google.adk.agents module
*   **Agent**
*   **BaseAgent**
    *   `after_agent_callback`
    *   `before_agent_callback`
    *   `description`
    *   `name`
    *   `parent_agent`
    *   `sub_agents`
    *   `config_type`
    *   `from_config()`
    *   `validate_name`
    *   `clone()`
    *   `find_agent()`
    *   `find_sub_agent()`
    *   `model_post_init()`
    *   `run_async()`
    *   `run_live()`
    *   `canonical_after_agent_callbacks`
    *   `canonical_before_agent_callbacks`
    *   `root_agent`
*   **InvocationContext**
    *   `active_streaming_tools`
    *   `agent`
    *   `agent_states`
    *   `artifact_service`
    *   `branch`
    *   `canonical_tools_cache`
    *   `context_cache_config`
    *   `credential_service`
    *   `end_invocation`
    *   `end_of_agents`
    *   `input_realtime_cache`
    *   `invocation_id`
    *   `live_request_queue`
    *   `live_session_resumption_handle`
    *   `memory_service`
    *   `output_realtime_cache`
    *   `plugin_manager`
    *   `resumability_config`
    *   `run_config`
    *   `session`
    *   `session_service`
    *   `transcription_cache`
    *   `user_content`
    *   `increment_llm_call_count()`
    *   `model_post_init()`
    *   `populate_invocation_agent_states()`
    *   `reset_sub_agent_states()`
    *   `set_agent_state()`
    *   `should_pause_invocation()`
    *   `app_name`
    *   `is_resumable`
    *   `user_id`
*   **LiveRequest**
    *   `activity_end`
    *   `activity_start`
    *   `blob`
    *   `close`
    *   `content`
*   **LiveRequestQueue**
    *   `close()`
    *   `get()`
    *   `send()`
    *   `send_activity_end()`
    *   `send_activity_start()`
    *   `send_content()`
    *   `send_realtime()`
*   **LlmAgent**
    *   `after_model_callback`
    *   `after_tool_callback`
    *   `before_model_callback`
    *   `before_tool_callback`
    *   `code_executor`
    *   `disallow_transfer_to_parent`
    *   `disallow_transfer_to_peers`
    *   `generate_content_config`
    *   `global_instruction`
    *   `include_contents`
    *   `input_schema`
    *   `instruction`
    *   `model`
    *   `on_model_error_callback`
    *   `on_tool_error_callback`
    *   `output_key`
    *   `output_schema`
    *   `planner`
    *   `static_instruction`
    *   `tools`
    *   `config_type`
    *   `validate_generate_content_config`
    *   `canonical_global_instruction()`
    *   `canonical_instruction()`
    *   `canonical_tools()`
    *   `canonical_after_model_callbacks`
    *   `canonical_after_tool_callbacks`
    *   `canonical_before_model_callbacks`
    *   `canonical_before_tool_callbacks`
    *   `canonical_model`
    *   `canonical_on_model_error_callbacks`
    *   `canonical_on_tool_error_callbacks`
*   **LoopAgent**
    *   `max_iterations`
    *   `config_type`
*   **McpInstructionProvider**
*   **ParallelAgent**
    *   `config_type`
*   **RunConfig**
    *   `context_window_compression`
    *   `custom_metadata`
    *   `enable_affective_dialog`
    *   `input_audio_transcription`
    *   `max_llm_calls`
    *   `output_audio_transcription`
    *   `proactivity`
    *   `realtime_input_config`
    *   `response_modalities`
    *   `save_live_blob`
    *   `session_resumption`
    *   `speech_config`
    *   `streaming_mode`
    *   `support_cfc`
    *   `check_for_deprecated_save_live_audio`
    *   `validate_max_llm_calls`
    *   `save_input_blobs_as_artifacts`
    *   `msg`
    *   `wrapped_property`
    *   `field_name`
    *   `save_live_audio`
*   **SequentialAgent**
    *   `config_type`

## google.adk.artifacts module
*   **BaseArtifactService**
    *   `delete_artifact()`
    *   `get_artifact_version()`
    *   `list_artifact_keys()`
    *   `list_artifact_versions()`
    *   `list_versions()`
    *   `load_artifact()`
    *   `save_artifact()`
*   **FileArtifactService**
    *   `delete_artifact()`
    *   `get_artifact_version()`
    *   `list_artifact_keys()`
    *   `list_artifact_versions()`
    *   `list_versions()`
    *   `load_artifact()`
    *   `save_artifact()`
*   **GcsArtifactService**
    *   `delete_artifact()`
    *   `get_artifact_version()`
    *   `list_artifact_keys()`
    *   `list_artifact_versions()`
    *   `list_versions()`
    *   `load_artifact()`
    *   `save_artifact()`
*   **InMemoryArtifactService**
    *   `artifacts`
    *   `delete_artifact()`
    *   `get_artifact_version()`
    *   `list_artifact_keys()`
    *   `list_artifact_versions()`
    *   `list_versions()`
    *   `load_artifact()`
    *   `save_artifact()`

## google.adk.apps package
*   **App**
    *   `context_cache_config`
    *   `events_compaction_config`
    *   `name`
    *   `plugins`
    *   `resumability_config`
    *   `root_agent`
*   **ResumabilityConfig**
    *   `is_resumable`

## google.adk.auth module
## google.adk.cli module
## google.adk.code_executors module
*   **BaseCodeExecutor**
    *   `optimize_data_file`
    *   `stateful`
    *   `error_retry_attempts`
    *   `code_block_delimiters`
    *   `execution_result_delimiters`
    *   `execute_code()`
*   **BuiltInCodeExecutor**
    *   `execute_code()`
    *   `process_llm_request()`
*   **CodeExecutorContext**
    *   `add_input_files()`
    *   `add_processed_file_names()`
    *   `clear_input_files()`
    *   `get_error_count()`
    *   `get_execution_id()`
    *   `get_input_files()`
    *   `get_processed_file_names()`
    *   `get_state_delta()`
    *   `increment_error_count()`
    *   `reset_error_count()`
    *   `set_execution_id()`
    *   `update_code_execution_result()`
*   **UnsafeLocalCodeExecutor**
    *   `optimize_data_file`
    *   `stateful`
    *   `execute_code()`

## google.adk.errors module
## google.adk.evaluation module
*   **AgentEvaluator**
    *   `evaluate()`
    *   `evaluate_eval_set()`
    *   `find_config_for_test_file()`
    *   `migrate_eval_data_to_new_schema()`

## google.adk.events module
*   **Event**
    *   `actions`
    *   `author`
    *   `branch`
    *   `id`
    *   `invocation_id`
    *   `long_running_tool_ids`
    *   `timestamp`
    *   `new_id()`
    *   `get_function_calls()`
    *   `get_function_responses()`
    *   `has_trailing_code_execution_result()`
    *   `is_final_response()`
    *   `model_post_init()`
*   **EventActions**
    *   `agent_state`
    *   `artifact_delta`
    *   `compaction`
    *   `end_of_agent`
    *   `escalate`
    *   `requested_auth_configs`
    *   `requested_tool_confirmations`
    *   `rewind_before_invocation_id`
    *   `skip_summarization`
    *   `state_delta`
    *   `transfer_to_agent`

## google.adk.examples module
*   **BaseExampleProvider**
    *   `get_examples()`
*   **Example**
    *   `input`
    *   `output`
*   **VertexAiExampleStore**
    *   `get_examples()`

## google.adk.flows module
## google.adk.memory module
*   **BaseMemoryService**
    *   `add_session_to_memory()`
    *   `search_memory()`
*   **InMemoryMemoryService**
    *   `add_session_to_memory()`
    *   `search_memory()`
*   **VertexAiMemoryBankService**
    *   `add_session_to_memory()`
    *   `search_memory()`
*   **VertexAiRagMemoryService**
    *   `add_session_to_memory()`
    *   `search_memory()`

## google.adk.models module
*   **BaseLlm**
    *   `model`
    *   `supported_models()`
    *   `connect()`
    *   `generate_content_async()`
*   **Gemini**
    *   `model`
    *   `retry_options`
    *   `speech_config`
    *   `supported_models()`
    *   `connect()`
    *   `generate_content_async()`
    *   `api_client`
*   **Gemma**
    *   `model`
    *   `supported_models()`
    *   `generate_content_async()`
*   **LLMRegistry**
    *   `new_llm()`
    *   `register()`
    *   `resolve()`

## google.adk.planners module
*   **BasePlanner**
    *   `build_planning_instruction()`
    *   `process_planning_response()`
*   **BuiltInPlanner**
    *   `thinking_config`
    *   `apply_thinking_config()`
    *   `build_planning_instruction()`
    *   `process_planning_response()`
*   **PlanReActPlanner**
    *   `build_planning_instruction()`
    *   `process_planning_response()`

## google.adk.platform module
## google.adk.plugins module
*   **BasePlugin**
    *   `after_agent_callback()`
    *   `after_model_callback()`
    *   `after_run_callback()`
    *   `after_tool_callback()`
    *   `before_agent_callback()`
    *   `before_model_callback()`
    *   `before_run_callback()`
    *   `before_tool_callback()`
    *   `close()`
    *   `on_event_callback()`
    *   `on_model_error_callback()`
    *   `on_tool_error_callback()`
    *   `on_user_message_callback()`
*   **LoggingPlugin**
    *   `after_agent_callback()`
    *   `after_model_callback()`
    *   `after_run_callback()`
    *   `after_tool_callback()`
    *   `before_agent_callback()`
    *   `before_model_callback()`
    *   `before_run_callback()`
    *   `before_tool_callback()`
    *   `on_event_callback()`
    *   `on_model_error_callback()`
    *   `on_tool_error_callback()`
    *   `on_user_message_callback()`
*   **PluginManager**
    *   `close()`
    *   `get_plugin()`
    *   `register_plugin()`
    *   `run_after_agent_callback()`
    *   `run_after_model_callback()`
    *   `run_after_run_callback()`
    *   `run_after_tool_callback()`
    *   `run_before_agent_callback()`
    *   `run_before_model_callback()`
    *   `run_before_run_callback()`
    *   `run_before_tool_callback()`
    *   `run_on_event_callback()`
    *   `run_on_model_error_callback()`
    *   `run_on_tool_error_callback()`
    *   `run_on_user_message_callback()`
*   **ReflectAndRetryToolPlugin**
    *   `after_tool_callback()`
    *   `extract_error_from_result()`
    *   `on_tool_error_callback()`

## google.adk.runners module
*   **InMemoryRunner**
    *   `agent`
    *   `app_name`
*   **Runner**
    *   `app_name`
    *   `agent`
    *   `artifact_service`
    *   `plugin_manager`
    *   `session_service`
    *   `memory_service`
    *   `credential_service`
    *   `context_cache_config`
    *   `resumability_config`
    *   `close()`
    *   `rewind_async()`
    *   `run()`
    *   `run_async()`
    *   `run_debug()`
    *   `run_live()`

## google.adk.sessions module
*   **BaseSessionService**
    *   `append_event()`
    *   `create_session()`
    *   `delete_session()`
    *   `get_session()`
    *   `list_sessions()`
*   **InMemorySessionService**
    *   `append_event()`
    *   `create_session()`
    *   `create_session_sync()`
    *   `delete_session()`
    *   `delete_session_sync()`
    *   `get_session()`
    *   `get_session_sync()`
    *   `list_sessions()`
    *   `list_sessions_sync()`
*   **Session**
    *   `app_name`
    *   `events`
    *   `id`
    *   `last_update_time`
    *   `state`
    *   `user_id`
*   **State**
    *   `APP_PREFIX`
    *   `TEMP_PREFIX`
    *   `USER_PREFIX`
    *   `get()`
    *   `has_delta()`
    *   `setdefault()`
    *   `to_dict()`
    *   `update()`
*   **VertexAiSessionService**
    *   `append_event()`
    *   `create_session()`
    *   `delete_session()`
    *   `get_session()`
    *   `list_sessions()`

## google.adk.telemetry module
*   `trace_call_llm()`
*   `trace_merged_tool_calls()`
*   `trace_send_data()`
*   `trace_tool_call()`

## google.adk.tools package
*   **APIHubToolset**
    *   `close()`
    *   `get_tools()`
*   **AgentTool**
    *   `agent`
    *   `skip_summarization`
    *   `from_config()`
    *   `populate_name()`
    *   `run_async()`
*   **AuthToolArguments**
    *   `auth_config`
    *   `function_call_id`
*   **BaseTool**
    *   `custom_metadata`
    *   `description`
    *   `from_config()`
    *   `is_long_running`
    *   `name`
    *   `process_llm_request()`
    *   `run_async()`
*   **DiscoveryEngineSearchTool**
    *   `discovery_engine_search()`
*   **ExampleTool**
    *   `examples`
    *   `from_config()`
    *   `process_llm_request()`
*   **FunctionTool**
    *   `func`
    *   `run_async()`
*   **LongRunningFunctionTool**
    *   `is_long_running`
*   **MCPToolset**
*   **McpToolset**
    *   `close()`
    *   `from_config()`
    *   `get_tools()`
*   **ToolContext**
    *   `invocation_context`
    *   `function_call_id`
    *   `event_actions`
    *   `tool_confirmation`
    *   `actions`
    *   `get_auth_response()`
    *   `request_confirmation()`
    *   `request_credential()`
    *   `search_memory()`
*   **VertexAiSearchTool**
    *   `data_store_id`
    *   `search_engine_id`
    *   `process_llm_request()`
*   `exit_loop()`
*   `transfer_to_agent()`

## google.adk.tools.agent_tool module
*   **AgentTool**
    *   `agent`
    *   `skip_summarization`
    *   `from_config()`
    *   `populate_name()`
    *   `run_async()`
*   **AgentToolConfig**
    *   `agent`
    *   `skip_summarization`

## google.adk.tools.apihub_tool module
*   **APIHubToolset**
    *   `close()`
    *   `get_tools()`

## google.adk.tools.application_integration_tool module
*   **ApplicationIntegrationToolset**
    *   `close()`
    *   `get_tools()`
*   **IntegrationConnectorTool**
    *   `EXCLUDE_FIELDS`
    *   `OPTIONAL_FIELDS`
    *   `run_async()`

## google.adk.tools.authenticated_function_tool module
*   **AuthenticatedFunctionTool**
    *   `run_async()`

## google.adk.tools.base_authenticated_tool module
*   **BaseAuthenticatedTool**
    *   `run_async()`

## google.adk.tools.base_tool module
*   **BaseTool**
    *   `custom_metadata`
    *   `description`
    *   `from_config()`
    *   `is_long_running`
    *   `name`
    *   `process_llm_request()`
    *   `run_async()`

## google.adk.tools.base_toolset module
*   **BaseToolset**
    *   `close()`
    *   `from_config()`
    *   `get_tools()`
    *   `get_tools_with_prefix()`
    *   `process_llm_request()`
*   **ToolPredicate**

## google.adk.tools.bigquery module
*   **BigQueryCredentialsConfig**
    *   `model_post_init()`
*   **BigQueryToolset**
    *   `close()`
    *   `get_tools()`

## google.adk.tools.crewai_tool module
*   **CrewaiTool**
    *   `from_config()`
    *   `run_async()`
    *   `tool`
*   **CrewaiToolConfig**
    *   `description`
    *   `name`
    *   `tool`

## google.adk.tools.enterprise_search_tool module
*   **EnterpriseWebSearchTool**
    *   `process_llm_request()`

## google.adk.tools.example_tool module
*   **ExampleTool**
    *   `examples`
    *   `from_config()`
    *   `process_llm_request()`
*   **ExampleToolConfig**
    *   `examples`

## google.adk.tools.exit_loop_tool module
*   `exit_loop()`

## google.adk.tools.function_tool module
*   **FunctionTool**
    *   `func`
    *   `run_async()`

## google.adk.tools.get_user_choice_tool module
*   `get_user_choice()`

## google.adk.tools.google_api_tool module
*   **BigQueryToolset**
*   **CalendarToolset**
*   **DocsToolset**
*   **GmailToolset**
*   **GoogleApiTool**
    *   `configure_auth()`
    *   `configure_sa_auth()`
    *   `run_async()`
*   **GoogleApiToolset**
    *   `close()`
    *   `configure_auth()`
    *   `configure_sa_auth()`
    *   `get_tools()`
    *   `set_tool_filter()`
*   **SheetsToolset**
*   **SlidesToolset**
*   **YoutubeToolset**

## google.adk.tools.google_maps_grounding_tool module
*   **GoogleMapsGroundingTool**
    *   `process_llm_request()`

## google.adk.tools.google_search_tool module
*   **GoogleSearchTool**
    *   `process_llm_request()`

## google.adk.tools.langchain_tool module
*   **LangchainTool**
    *   `from_config()`
*   **LangchainToolConfig**
    *   `description`
    *   `name`
    *   `tool`

## google.adk.tools.load_artifacts_tool module
*   **LoadArtifactsTool**
    *   `process_llm_request()`
    *   `run_async()`

## google.adk.tools.load_memory_tool module
*   **LoadMemoryResponse**
    *   `memories`
*   **LoadMemoryTool**
    *   `process_llm_request()`
*   `load_memory()`

## google.adk.tools.load_web_page module
*   `load_web_page()`

## google.adk.tools.long_running_tool module
*   **LongRunningFunctionTool**
    *   `is_long_running`

## google.adk.tools.mcp_tool module
*   **MCPTool**
*   **MCPToolset**
*   **McpTool**
    *   `raw_mcp_tool`
    *   `run_async()`
*   **McpToolset**
    *   `close()`
    *   `from_config()`
    *   `get_tools()`
*   **SseConnectionParams**
    *   `url`
    *   `headers`
    *   `timeout`
    *   `sse_read_timeout`
*   **StdioConnectionParams**
    *   `server_params`
    *   `timeout`
*   **StreamableHTTPConnectionParams**
    *   `url`
    *   `headers`
    *   `timeout`
    *   `sse_read_timeout`
    *   `terminate_on_close`
*   `adk_to_mcp_tool_type()`
*   `gemini_to_json_schema()`

## google.adk.tools.openapi_tool module
*   **OpenAPIToolset**
    *   `close()`
    *   `get_tool()`
    *   `get_tools()`
*   **RestApiTool**
    *   `call()`
    *   `configure_auth_credential()`
    *   `configure_auth_scheme()`
    *   `from_parsed_operation()`
    *   `from_parsed_operation_str()`
    *   `run_async()`
    *   `set_default_headers()`

## google.adk.tools.preload_memory_tool module
*   **PreloadMemoryTool**
    *   `process_llm_request()`

## google.adk.tools.retrieval module
*   **BaseRetrievalTool**

## google.adk.tools.tool_context module
*   **ToolContext**
    *   `invocation_context`
    *   `function_call_id`
    *   `event_actions`
    *   `tool_confirmation`
    *   `actions`
    *   `get_auth_response()`
    *   `request_confirmation()`
    *   `request_credential()`
    *   `search_memory()`

## google.adk.tools.toolbox_toolset module
*   **ToolboxToolset**
    *   `close()`
    *   `get_tools()`

## google.adk.tools.transfer_to_agent_tool module
*   `transfer_to_agent()`

## google.adk.tools.url_context_tool module
*   **UrlContextTool**
    *   `process_llm_request()`

## google.adk.tools.vertex_ai_search_tool module
*   **VertexAiSearchTool**
    *   `data_store_id`
    *   `search_engine_id`
    *   `process_llm_request()`

## google.adk.utils module
## google.adk.version module
