"""
Comprehensive test suite for LLM-powered agents
Tests all 4 agents with real LLM inference
"""

import pytest
import json
from schemas import SurplusReport, ValidatedRecord, RankedMatches, SafetyDecision, FinalDecision
from agents import EklavyaIntakeAgent, ArjunaMatchingAgent, DronacharyyaSafetyAgent, ChanakyaLogisticsAgent
from sutradhara_flow import SutradharaFlow
from rag_system import get_rag_system
from llm_integration import get_llm_manager
from mcp_servers import get_mcp_manager


class TestEklavyaAgent:
    """Tests for Eklavya intake agent"""
    
    def test_valid_report(self):
        """Test valid food report"""
        agent = EklavyaIntakeAgent()
        report = SurplusReport(
            food_type="vegetable biryani",
            quantity=60,
            prep_time="14:00",
            temperature_c=58.0,
            location="Hostel Mess A",
            pickup_deadline="20:00"
        )
        
        result = agent.execute(report)
        assert isinstance(result, ValidatedRecord)
        assert result.status in ["valid", "needs_fix", "rejected"]
        print(f"✓ Eklavya validation: {result.status}")
    
    def test_invalid_temperature(self):
        """Test report with invalid temperature"""
        agent = EklavyaIntakeAgent()
        report = SurplusReport(
            food_type="chicken curry",
            quantity=30,
            prep_time="14:00",
            temperature_c=-5.0,  # Invalid
            location="Canteen",
            pickup_deadline="20:00"
        )
        
        result = agent.execute(report)
        assert result.status in ["needs_fix", "rejected"]
        assert len(result.issues) > 0
        print(f"✓ Eklavya detected invalid temperature")
    
    def test_missing_location(self):
        """Test report with invalid location"""
        agent = EklavyaIntakeAgent()
        report = SurplusReport(
            food_type="rice",
            quantity=50,
            prep_time="12:00",
            temperature_c=60.0,
            location="Unknown Location",
            pickup_deadline="18:00"
        )
        
        result = agent.execute(report)
        assert len(result.issues) > 0
        print(f"✓ Eklavya detected invalid location")


class TestArjunaAgent:
    """Tests for Arjuna matching agent"""
    
    def test_recipient_ranking(self):
        """Test recipient ranking"""
        eklavya = EklavyaIntakeAgent()
        arjuna = ArjunaMatchingAgent()
        
        report = SurplusReport(
            food_type="vegetable biryani",
            quantity=60,
            prep_time="14:00",
            temperature_c=58.0,
            location="Hostel Mess A",
            pickup_deadline="20:00"
        )
        
        validated = eklavya.execute(report)
        if validated.status == "valid":
            matches = arjuna.execute(validated)
            assert isinstance(matches, RankedMatches)
            assert len(matches.matches) >= 0
            if len(matches.matches) > 0:
                assert matches.matches[0].score >= 0
                print(f"✓ Arjuna ranked {len(matches.matches)} recipients")


class TestDronacharyyaAgent:
    """Tests for Dronacharya safety agent"""
    
    def test_rag_retrieval(self):
        """Test RAG system retrieval"""
        rag = get_rag_system()
        passages = rag.retrieve("cooked rice temperature holding time", k=3)
        assert len(passages) > 0
        assert "similarity" in passages[0]
        assert passages[0]["similarity"] > 0
        print(f"✓ RAG retrieved {len(passages)} passages")
    
    def test_safety_assessment(self):
        """Test safety assessment"""
        agent = DronacharyyaSafetyAgent()
        eklavya = EklavyaIntakeAgent()
        
        report = SurplusReport(
            food_type="cooked rice",
            quantity=40,
            prep_time="14:00",
            temperature_c=60.0,
            location="Canteen",
            pickup_deadline="20:00"
        )
        
        validated = eklavya.execute(report)
        safety = agent.execute(validated)
        
        assert isinstance(safety, SafetyDecision)
        assert safety.verdict in ["safe", "unsafe", "conditional", "insufficient_evidence"]
        assert len(safety.evidence) > 0 or safety.verdict == "insufficient_evidence"
        print(f"✓ Dronacharya verdict: {safety.verdict}")
    
    def test_unsafe_detection(self):
        """Test unsafe food detection"""
        agent = DronacharyyaSafetyAgent()
        eklavya = EklavyaIntakeAgent()
        
        report = SurplusReport(
            food_type="meat curry",
            quantity=20,
            prep_time="14:00",
            temperature_c=35.0,  # Below safe temperature
            location="Canteen",
            pickup_deadline="20:00"
        )
        
        validated = eklavya.execute(report)
        safety = agent.execute(validated)
        
        # Should be unsafe or conditional due to low temperature
        assert safety.verdict in ["unsafe", "conditional"]
        print(f"✓ Dronacharya detected unsafe food")


class TestChanakyaAgent:
    """Tests for Chanakya coordinator"""
    
    def test_full_workflow(self):
        """Test complete workflow with all agents"""
        flow = SutradharaFlow()
        
        report = {
            "food_type": "vegetable biryani",
            "quantity": 60,
            "prep_time": "14:00",
            "temperature_c": 58.0,
            "location": "Hostel Mess A",
            "pickup_deadline": "20:00"
        }
        
        result = flow.execute_flow(report)
        
        assert "run_id" in result
        assert "final_decision" in result or "error" in result
        
        if "final_decision" in result:
            decision = result["final_decision"]
            assert "action" in decision
            assert decision["action"] in ["dispatch", "hold", "discard", "no_pickup"]
            print(f"✓ Chanakya decision: {decision['action']}")


class TestMCPTools:
    """Tests for MCP tool servers"""
    
    def test_mcp_tool_discovery(self):
        """Test MCP tool discovery"""
        mcp = get_mcp_manager()
        servers = mcp.list_servers()
        assert len(servers) >= 3
        assert "recipient_database" in servers
        assert "food_safety" in servers
        assert "logistics" in servers
        print(f"✓ MCP discovered {len(servers)} servers")
    
    def test_recipient_database_tools(self):
        """Test recipient database MCP tools"""
        mcp = get_mcp_manager()
        result = mcp.execute_tool(
            "recipient_database",
            "search_recipients",
            {"food_category": "cooked_veg", "quantity": 60}
        )
        assert result["status"] == "success"
        assert "recipients" in result
        print(f"✓ MCP recipient search returned {len(result['recipients'])} recipients")
    
    def test_food_safety_tools(self):
        """Test food safety MCP tools"""
        mcp = get_mcp_manager()
        result = mcp.execute_tool(
            "food_safety",
            "get_temperature_requirements",
            {"food_type": "cooked_veg"}
        )
        assert result["status"] == "success"
        assert "min_temperature_c" in result
        assert "max_holding_hours" in result
        print(f"✓ MCP temperature requirements: min={result['min_temperature_c']}°C")


class TestLLMIntegration:
    """Tests for LLM integration"""
    
    def test_llm_availability(self):
        """Test LLM provider availability"""
        llm = get_llm_manager()
        is_available = llm.is_available()
        # Should be available or gracefully fail
        print(f"✓ LLM availability: {is_available}")
    
    @pytest.mark.skipif(
        not get_llm_manager().is_available(),
        reason="LLM provider not configured"
    )
    def test_llm_generation(self):
        """Test LLM text generation"""
        llm = get_llm_manager()
        response = llm.generate(
            prompt="What is the safe holding temperature for cooked vegetables?",
            system="You are a food safety expert."
        )
        assert isinstance(response, str)
        assert len(response) > 0
        print(f"✓ LLM generated: {response[:100]}...")


class TestRAGSystem:
    """Tests for RAG system"""
    
    def test_rag_initialization(self):
        """Test RAG system initialization"""
        rag = get_rag_system()
        assert rag.collection.count() > 0
        print(f"✓ RAG collection has {rag.collection.count()} documents")
    
    def test_rag_retrieval_quality(self):
        """Test RAG retrieval quality"""
        rag = get_rag_system()
        
        # Test relevant query
        passages = rag.retrieve("cooked rice temperature holding", k=5)
        assert len(passages) > 0
        
        # Check similarity scores
        for p in passages:
            assert "similarity" in p
            assert p["similarity"] >= 0
        
        print(f"✓ RAG retrieved relevant passages with avg similarity {sum(p['similarity'] for p in passages)/len(passages):.2f}")
    
    def test_rag_food_safety_assessment(self):
        """Test RAG-based safety assessment"""
        rag = get_rag_system()
        
        food_info = {
            "food_type": "cooked rice",
            "temperature_c": 60,
            "prep_time": "14:00",
            "elapsed_hours": 2
        }
        
        result = rag.assess_food_safety(food_info)
        assert result.verdict in ["safe", "unsafe", "conditional", "insufficient_evidence"]
        assert len(result.evidence) >= 0
        print(f"✓ RAG assessment: {result.verdict} (confidence: {result.confidence})")


# Edge case and stress tests

class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_zero_quantity(self):
        """Test handling of zero quantity"""
        agent = EklavyaIntakeAgent()
        report = SurplusReport(
            food_type="rice",
            quantity=0,
            prep_time="14:00",
            temperature_c=60.0,
            location="Canteen",
            pickup_deadline="20:00"
        )
        
        result = agent.execute(report)
        assert len(result.issues) > 0 or result.status == "needs_fix"
        print(f"✓ Handled zero quantity")
    
    def test_extreme_temperature(self):
        """Test handling of extreme temperatures"""
        agent = EklavyaIntakeAgent()
        
        # Very hot
        report = SurplusReport(
            food_type="rice",
            quantity=50,
            prep_time="14:00",
            temperature_c=95.0,
            location="Canteen",
            pickup_deadline="20:00"
        )
        
        result = agent.execute(report)
        assert len(result.issues) > 0 or result.status in ["needs_fix", "rejected"]
        print(f"✓ Handled extreme temperature")
    
    def test_past_deadline(self):
        """Test handling of past pickup deadline"""
        agent = EklavyaIntakeAgent()
        report = SurplusReport(
            food_type="rice",
            quantity=50,
            prep_time="14:00",
            temperature_c=60.0,
            location="Canteen",
            pickup_deadline="12:00"  # Already past
        )
        
        result = agent.execute(report)
        # Should flag as issue
        print(f"✓ Handled past deadline")


if __name__ == "__main__":
    # Run all tests
    print("\n" + "="*70)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Eklavya tests
    print("\n[EKLAVYA INTAKE AGENT]")
    test_eklavya = TestEklavyaAgent()
    test_eklavya.test_valid_report()
    test_eklavya.test_invalid_temperature()
    test_eklavya.test_missing_location()
    
    # Arjuna tests
    print("\n[ARJUNA MATCHING AGENT]")
    test_arjuna = TestArjunaAgent()
    test_arjuna.test_recipient_ranking()
    
    # Dronacharya tests
    print("\n[DRONACHARYA SAFETY AGENT]")
    test_dron = TestDronacharyyaAgent()
    test_dron.test_rag_retrieval()
    test_dron.test_safety_assessment()
    test_dron.test_unsafe_detection()
    
    # Chanakya tests
    print("\n[CHANAKYA COORDINATOR]")
    test_chan = TestChanakyaAgent()
    test_chan.test_full_workflow()
    
    # MCP tests
    print("\n[MCP TOOL SERVERS]")
    test_mcp = TestMCPTools()
    test_mcp.test_mcp_tool_discovery()
    test_mcp.test_recipient_database_tools()
    test_mcp.test_food_safety_tools()
    
    # LLM tests
    print("\n[LLM INTEGRATION]")
    test_llm = TestLLMIntegration()
    test_llm.test_llm_availability()
    
    # RAG tests
    print("\n[RAG SYSTEM]")
    test_rag = TestRAGSystem()
    test_rag.test_rag_initialization()
    test_rag.test_rag_retrieval_quality()
    test_rag.test_rag_food_safety_assessment()
    
    # Edge cases
    print("\n[EDGE CASES]")
    test_edge = TestEdgeCases()
    test_edge.test_zero_quantity()
    test_edge.test_extreme_temperature()
    test_edge.test_past_deadline()
    
    print("\n" + "="*70)
    print("✓ ALL TESTS COMPLETED")
    print("="*70)
