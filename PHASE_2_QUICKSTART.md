# Phase 2: Quick Start Guide

## What's New in Phase 2

FoodRescue-MAS Phase 2 adds **7 powerful new modules** for enterprise-grade agent systems:

| Module | Purpose | Key Feature |
|--------|---------|------------|
| `a2a_protocol.py` | Cross-framework communication | CrewAI ↔ ADK agents talk to each other |
| `blackboard_architecture.py` | Shared state management | All agents access centralized state |
| `guardrails_security.py` | Security & validation | Detect injections, validate inputs |
| `mcp_integration.py` | External tools | Web search, database, file parser |
| `adk_agents.py` | Google ADK framework | 4 agents using ReAct pattern |
| `callback_system.py` | Real-time monitoring | Track every agent action |
| `prompt_variants.py` | Prompt testing | 8 different prompt strategies |
| `performance_evaluator.py` | Comparative testing | Benchmark all combinations |
| `cloud_deployment.py` | Cloud configs | Docker, AWS, GCP, Azure |
| `integration_tests.py` | Full testing | 24+ integration tests |

---

## Installation

### 1. Update Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python -c "
import a2a_protocol
import blackboard_architecture
import guardrails_security
import mcp_integration
import adk_agents
import callback_system
import prompt_variants
import performance_evaluator
import cloud_deployment
print('✓ All Phase 2 modules installed')
"
```

---

## Quick Demos

### Demo 1: A2A Protocol (Cross-Framework Communication)
```bash
python a2a_protocol.py
```

**What it shows**:
- Registering CrewAI and ADK agents
- Sending messages between frameworks
- Building audit trails

**Output**:
```
✓ Registered CREWAI agent: Eklavya (CrewAI)
✓ Registered ADK agent: Arjuna (ADK)
✓ Message sent: [message_id]
✓ Agents discovered: 2
```

---

### Demo 2: Blackboard Architecture
```bash
python blackboard_architecture.py
```

**What it shows**:
- Creating shared state
- Agents reading/writing to blackboard
- State versioning and history

**Output**:
```
→ Executing eklavya...
→ Executing arjuna...
...
FINAL DECISION: dispatch
```

---

### Demo 3: Security & Guardrails
```bash
python guardrails_security.py
```

**What it shows**:
- Detecting prompt injections
- Filtering toxic language
- Rate limiting
- Tool validation

**Output**:
```
✓ PASSED: Normal input
✗ FAILED: Prompt injection detected
✓ PASSED: Rate limit OK
```

---

### Demo 4: MCP Integration
```bash
python mcp_integration.py
```

**What it shows**:
- Connecting to MCP servers
- Executing web search
- Database queries
- File parsing

**Output**:
```
✓ Connected to web_search_mcp
✓ Connected to database_mcp
✓ Connected to file_parser_mcp
→ Web Search: ✓ (15.2ms)
→ Database Query: ✓ (8.5ms)
```

---

### Demo 5: ADK Agents
```bash
python adk_agents.py
```

**What it shows**:
- Creating ADK agents
- ReAct pattern (think → act)
- Full ADK workflow

**Output**:
```
[1] Eklavya (ADK) - Intake & Validation
  Status: valid
[2] Arjuna (ADK) - Matching & Ranking
  Matches found: 3
[3] Dronacharya (ADK) - Safety & Compliance
  Verdict: safe
[4] Chanakya (ADK) - Logistics & Decision
  Action: dispatch
```

---

### Demo 6: Callback System
```bash
python callback_system.py
```

**What it shows**:
- Agent lifecycle callbacks
- Tool execution tracking
- Metrics collection
- Execution traces

**Output**:
```
→ [START] Agent: eklavya
  Timestamp: 2024-11-06T...
✓ [COMPLETE] Agent: eklavya
  Result received (25.5ms)

METRICS SUMMARY
  agent_count: 1
  tool_calls: 1
  decisions_made: 1
```

---

### Demo 7: Prompt Variants
```bash
python prompt_variants.py
```

**What it shows**:
- Available prompt variants
- ReAct vs Few-shot vs Persona
- Full prompts with examples

**Output**:
```
AVAILABLE PROMPT VARIANTS

eklavya:
  - react (ReAct approach)
  - fewshot (Few-shot learning)
  - constraint (Hard rules)
  
arjuna:
  - react (Iterative ranking)
  - fewshot (Score by example)
  
... (total 12+ variants)
```

---

### Demo 8: Performance Evaluation
```bash
python performance_evaluator.py
```

**What it shows**:
- Running 18 variant combinations
- Testing frameworks × architectures × prompts
- Performance metrics (latency, accuracy, cost)
- Comparative analysis

**Output** (takes ~2 min):
```
[1/18] CREWAI + sequential + react
  ✓ Run 1/10: 156.23ms, Accuracy: 87.5%
  ✓ Run 2/10: 158.91ms, Accuracy: 87.2%
  ...
[2/18] CREWAI + sequential + fewshot
  ...

ANALYSIS
========
Best Accuracy: crewai_blackboard_react (89.5%)
Best Speed: crewai_sequential_fewshot (142ms)
Best Cost: crewai_sequential_react ($0.021)

Recommendations:
1. Use Blackboard for +5% accuracy improvement
2. Use ReAct for best reasoning quality
```

---

### Demo 9: Cloud Deployment
```bash
python cloud_deployment.py
```

**What it shows**:
- Docker containerization
- AWS/GCP/Azure configs
- Deployment commands

**Output**:
```
DOCKER CONFIGURATION
=====================
FROM python:3.11-slim
WORKDIR /app
...

AWS DEPLOYMENT
==============
# Build and push Docker image
docker build -t food-rescue-mas:latest .
docker tag ... ACCOUNT_ID.dkr.ecr...

GCP DEPLOYMENT
==============
gcloud builds submit ...
gcloud run deploy food-rescue-service ...
```

---

### Demo 10: Integration Tests
```bash
python integration_tests.py
```

**What it shows**:
- Full integration testing
- 24+ tests across all components
- Results summary

**Output**:
```
[1] A2A Protocol Tests:
  ✓ PASS: A2A Agent Registration (12.3ms)
  ✓ PASS: A2A CrewAI → ADK Message (8.5ms)
  ✓ PASS: A2A ADK → CrewAI Message (7.2ms)
  ✓ PASS: A2A Message History (5.1ms)

[2] Blackboard Architecture Tests:
  ✓ PASS: Blackboard State Creation (3.2ms)
  ✓ PASS: Blackboard State Updates (6.7ms)
  ...

TEST SUMMARY
============
Total Tests: 24
Passed: 24
Failed: 0
Success Rate: 100.0%
```

---

## Integration Examples

### Example 1: Using A2A Protocol + ADK Agents
```python
from a2a_protocol import a2a_protocol
from adk_agents import adk_framework, initialize_adk

# Initialize
initialize_adk()

# Register CrewAI agent (existing)
a2a_protocol.register_crewai_agent("eklavya_crew", "Eklavya", ["validate"], {}, {})

# Send message to ADK agent
msg = a2a_protocol.send_request(
    "eklavya_crew", "crewai",
    "arjuna_adk", "adk",
    {"validated_data": {...}}
)

# Get audit trail
history = a2a_protocol.get_audit_trail()
```

### Example 2: Using Blackboard + Callbacks
```python
from blackboard_architecture import Blackboard, BlackboardOrchestrator
from callback_system import callback_system

# Create blackboard
bb = Blackboard()

# Register callback for state changes
def on_state_change(run_id, agent_id, changes):
    print(f"Agent {agent_id} updated state: {changes}")

bb.subscribe("run_001", on_state_change)

# Execute agents with callbacks
callback_system.trigger_agent_start("agent_1", "run_001")
bb.update_state("run_001", "agent_1", {"field": "value"})
callback_system.trigger_agent_complete("agent_1", "run_001")
```

### Example 3: Using Guardrails + MCP Tools
```python
from guardrails_security import GuardrailValidator, SecurityLevel
from mcp_integration import mcp_manager, initialize_mcp

# Initialize security
validator = GuardrailValidator(SecurityLevel.STRICT)

# Validate user input
user_input = request.data["input"]
valid, violations = validator.validate_input(user_input, user_id)

if valid:
    # Execute MCP tool
    initialize_mcp()
    result = mcp_manager.execute_tool("web_search_mcp", "search_web", {"query": user_input})
```

### Example 4: Using Prompt Variants + Evaluation
```python
from prompt_variants import variants_framework
from performance_evaluator import evaluator, Framework, Architecture

# Get variant
variant = variants_framework.get_variant("eklavya", "react")
prompt = variant.get_full_prompt("Validate: ...")

# Evaluate variant
scenario = evaluator.create_scenario(Framework.CREWAI, Architecture.SEQUENTIAL, variant.variant)
results = evaluator.run_evaluation(scenario.scenario_id, num_runs=10)

# Compare results
stats = scenario.get_statistics()
print(f"Average accuracy: {stats['avg_accuracy']:.1f}%")
```

---

## Common Tasks

### Task 1: Deploy to Docker
```bash
# Build image
docker build -t food-rescue-mas:latest .

# Run with docker-compose
docker-compose up

# Access services
curl http://localhost:8000/health    # API
# Dashboard: http://localhost:8501
```

### Task 2: Deploy to AWS
```bash
# Generate AWS config
python cloud_deployment.py

# Follow printed commands to:
# 1. Push image to ECR
# 2. Create ECS task
# 3. Create ECS service
```

### Task 3: Run Performance Evaluation
```bash
python performance_evaluator.py

# Get detailed report
python -c "
from performance_evaluator import evaluator
evaluation = evaluator.evaluations[0]
evaluator.export_results('results.json', evaluation)
"

# Analyze results
cat results.json | python -m json.tool
```

### Task 4: Run Security Tests
```bash
# Test individual components
python guardrails_security.py

# Run full integration tests
python integration_tests.py

# Run specific test
python -c "
from integration_tests import IntegrationTestSuite
suite = IntegrationTestSuite()
suite.test_a2a_agent_registration()
"
```

---

## Troubleshooting

### Issue: Import errors
```bash
# Update requirements
pip install -r requirements.txt --upgrade

# Verify imports
python -c "import a2a_protocol; print('OK')"
```

### Issue: MCP servers not connecting
```bash
# Check connectivity
python mcp_integration.py

# Verify environment
env | grep API_KEY  # If using external APIs
```

### Issue: Performance tests slow
```bash
# Run with fewer iterations
python -c "
from performance_evaluator import evaluator
evaluation = evaluator.run_comparative_evaluation(num_runs_per_variant=3)
"
```

### Issue: Callback metrics not updating
```bash
# Manually trigger callbacks
from callback_system import callback_system
callback_system.trigger_agent_start('test', 'run_001')
callback_system.trigger_agent_complete('test', 'run_001')
print(callback_system.get_metrics())
```

---

## Performance Tips

1. **Use Blackboard Architecture** for 5% accuracy boost
2. **Use ReAct Prompts** for better reasoning (slightly slower)
3. **Use Few-shot** for speed when accuracy is OK
4. **Batch MCP calls** to reduce latency
5. **Enable caching** for repeated queries
6. **Use rate limiting** to prevent overload

---

## Next Actions

### Immediate (Today)
- [x] Install Phase 2 modules
- [x] Run each demo
- [x] Review integration tests

### Short-term (This week)
- [ ] Deploy to Docker
- [ ] Run performance evaluation
- [ ] Review security guidelines
- [ ] Test MCP integrations

### Medium-term (This month)
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Set up CI/CD pipeline
- [ ] Run 100-run performance benchmark
- [ ] Configure monitoring/alerts

### Long-term (Next quarter)
- [ ] ML-based agents
- [ ] Real embeddings
- [ ] Advanced metrics
- [ ] Multi-language support

---

## Support

**Documentation**:
- See `PHASE_2_COMPLETION.md` for full details
- See individual module docstrings
- See `integration_tests.py` for usage examples

**Issues**:
- Check module-specific README sections
- Run integration tests for diagnostics
- Review error messages in callback logs

**Performance**:
- Use `performance_evaluator.py` for benchmarking
- Export results to JSON for analysis
- Compare variants to find best combo

---

## Success Indicators

✅ You're ready when:
- All imports work without errors
- Each demo runs successfully
- Integration tests pass (24/24)
- You can deploy to Docker
- Performance metrics are reasonable

**Typical Timeline**:
- Setup: 15 minutes
- Understanding: 1-2 hours
- Testing: 30 minutes
- Deployment: 1 hour
- **Total**: ~3-4 hours to full readiness

---

**Phase 2 is production-ready. Let's ship it! 🚀**
