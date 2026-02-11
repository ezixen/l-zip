"""
L-ZIP Example Prompts for VS Code Development

This file shows efficient L-ZIP formatted prompts for common development tasks.
Use these as templates for your own coding requests.

Author: ezixen
"""

# ============================================================================
# CODE DEVELOPMENT PROMPTS
# ============================================================================

PROMPT_1_CODE_GENERATION = """
ACT:Senior_Dev [Lang:Python] OBJ:Write_Function [Purpose:Token_Counter] 
THINK:StepByStep OUT:Production_Code + Docstring + Tests
"""
# Explanation: Act as senior developer, write Python function for token counting,
# use step-by-step reasoning, output production code with docstring and tests

PROMPT_2_CODE_REVIEW = """
ACT:Architect [Expertise:Performance+Security] CTX:[Code_Block] OBJ:Review_Code | Identify_Issues
EVAL:Performance_Bottlenecks+Security_Risks | Suggest_Improvements
GEN:Refactored_Code OUT:Detailed_Report
"""
# Explanation: Architecture expert reviews code for perf & security issues,
# suggests improvements, provides refactored version with detailed report

PROMPT_3_DEBUG_ISSUE = """
ACT:DevOps [Service:API] CTX:[Error_Log] OBJ:Find_RootCause + Provide_Fix 
THINK:StepByStep | Explain_Why
OUT:Solution + Prevention_Strategy
"""
# Explanation: DevOps expert analyzes error logs, explains root cause step-by-step,
# provides fix and future prevention strategy

PROMPT_4_REFACTORING = """
ACT:Software_Architect [Focus:Readability+Performance] CTX:[Code_Path] 
OBJ:Optimize_Code + Improve_Structure | Reduce_Complexity
LIM:No_Breaking_Changes GEN:Refactored_Code OUT:Diff + Explanation
"""
# Explanation: Architecture expert refactors code, improves readability/performance,
# ensures no breaking changes, outputs diff with explanation

PROMPT_5_TESTING = """
ACT:QA_Engineer [Framework:Pytest] CTX:[Codebase] OBJ:Create_ComprehensiveTests
LIM:80%_Coverage GEN:Test_Suite [Coverage:Unit+Integration] 
OUT:Python_Code + Test_Report
"""
# Explanation: QA engineer creates comprehensive test suite using Pytest,
# targeting 80% coverage, includes unit and integration tests


# ============================================================================
# DOCUMENTATION PROMPTS
# ============================================================================

PROMPT_6_API_DOCUMENTATION = """
ACT:Technical_Writer [Audience:Developers] CTX:[API_Spec] OBJ:Write_Docs
INCLUDE:[Examples, UseCases, ErrorHandling, Limitations]
LEN:2000w LIM:Concise+Practical OUT:Markdown + Code_Examples
"""
# Explanation: Technical writer creates comprehensive API documentation for developers,
# includes examples and error handling, concise and practical style

PROMPT_7_README_GENERATION = """
ACT:Developer [Role:Project_Lead] OBJ:Create_README [Project:L-ZIP]
SUM:[Features, Installation, QuickStart, Examples, Contributing]
OUT:Markdown + Badges + TOC
"""
# Explanation: Create README with features, installation, quick start, examples,
# includes badges and table of contents

PROMPT_8_CHANGELOG = """
ACT:Release_Manager OBJ:Document_Changes [Version:1.0.0] [Type:Initial_Release]
SUM:[Added, Changed, Deprecated, Removed, Fixed, Security]
OUT:Structured_Markdown
"""
# Explanation: Release manager documents version changes across all categories


# ============================================================================
# ANALYSIS & RESEARCH PROMPTS
# ============================================================================

PROMPT_9_PERFORMANCE_ANALYSIS = """
ACT:Performance_Engineer CTX:[Metrics_Data] OBJ:Analyze_Performance
EVAL:[Bottlenecks, Optimization_Opportunities, Comparative_Analysis]
SUM:Top5_Issues => Recommendations OUT:Report + Visualizations
"""
# Explanation: Performance engineer analyzes metrics, identifies bottlenecks,
# provides recommendations, outputs report with visualizations

PROMPT_10_SECURITY_AUDIT = """
ACT:Security_Specialist CTX:[Codebase] OBJ:Security_Audit
EVAL:[Vulnerabilities, Risks, Compliance_Issues]
SUM:Critical+High+Medium THINK:Manual_Review OUT:Audit_Report + Fix_Guide
"""
# Explanation: Security specialist audits codebase, evaluates vulnerabilities,
# provide audit report with fix guide organized by severity


# ============================================================================
# DESIGN & ARCHITECTURE PROMPTS
# ============================================================================

PROMPT_11_SYSTEM_DESIGN = """
ACT:Solutions_Architect [Scale:Enterprise] CTX:[Requirements] OBJ:Design_System
THINK:Scalability+Reliability+Performance
OUT:[Architecture_Diagram, Components, Data_Flow, Decisions]
VIS:System_Architecture_Diagram
"""
# Explanation: Solutions architect designs enterprise system considering scalability,
# provides architecture diagram, components, data flow, and design decisions

PROMPT_12_DATABASE_SCHEMA = """
ACT:Database_Architect [DB:PostgreSQL] OBJ:Design_Schema [Domain:Ecommerce]
CONSIDER:[Normalization, Indexes, Relationships, Performance, Scalability]
GEN:SQL_DDL_Statements OUT:Schema_Diagram + Explanation
VIS:[ER_Diagram, Relationship_Map]
"""
# Explanation: DB architect designs schema for ecommerce domain,
# generates SQL with ER diagram showing relationships


# ============================================================================
# PROJECT MANAGEMENT PROMPTS
# ============================================================================

PROMPT_13_PROJECT_PLANNING = """
ACT:Project_Manager [Methodology:Agile] OBJ:Create_Plan [Project:L-ZIP]
CTX:[Scope, Timeline, Budget, Resources] @6months
OUT:[Roadmap, Milestones, Timeline, Risk_Analysis]
SUM:Critical_Path => Dependencies
"""
# Explanation: Project manager creates 6-month plan with roadmap, milestones,
# timeline, risk analysis, and critical path dependencies

PROMPT_14_REQUIREMENTS_ANALYSIS = """
ACT:Business_Analyst [Domain:SaaS] CTX:[Stakeholder_Input] OBJ:Define_Requirements
EVAL:[Feasibility, Priority, Dependencies, Risks]
GEN:[User_Stories, Acceptance_Criteria] SUM:Top_Requirements
OUT:Requirements_Document + Prioritization_Matrix
"""
# Explanation: Business analyst defines requirements, evaluates feasibility,
# generates user stories and acceptance criteria, outputs prioritized requirements


# ============================================================================
# CONTENT & MARKETING PROMPTS
# ============================================================================

PROMPT_15_BLOG_POST = """
ACT:Technical_Writer [Audience:Developers] OBJ:Write_BlogPost [Topic:L-ZIP]
CTX:[Target:Beginner_to_Intermediate] @Practical_Focus
LEN:1500w LIM:Engaging+Clear + SEO_Friendly
OUT:Markdown + Social_Summary + Meta_Tags
"""
# Explanation: Technical writer creates 1500-word blog post about L-ZIP for developers,
# practical focus, includes social summary and meta tags

PROMPT_16_MARKETING_COPY = """
ACT:Copywriter [Tone:Professional+Friendly] OBJ:Create_Marketing_Content [Product:L-ZIP]
CTX:[Target_Audience:AI_Developers, Value_Prop:Token_Savings]
LIM:Compelling + Conversion_Focused LEN:<200w
OUT:Email_Copy + Landing_Page_Text + Social_Posts
"""
# Explanation: Copywriter creates marketing content emphasizing token savings,
# professional and friendly tone, outputs email, landing page, and social content


# ============================================================================
# LEARNING & EXPLANATION PROMPTS
# ============================================================================

PROMPT_17_CONCEPT_EXPLANATION = """
ACT:Educator [Level:Intermediate] OBJ:Explain_Concept [Topic:Token_Compression]
@Developer_Audience THINK:Analogies + Real_Examples
LIM:Clear+Concise LEN:500w
OUT:Explanation + Code_Example + Visual_Diagram
"""
# Explanation: Educator explains token compression concept using analogies and examples,
# includes code example and visual diagram

PROMPT_18_TUTORIAL = """
ACT:Instructor [Framework:L-ZIP] OBJ:Create_Tutorial [Goal:Getting_Started]
STEP:[1_Installation, 2_HelloWorld, 3_MyFirstPrompt, 4_Advanced]
GEN:[Code_Snippets, Screenshots, Explanations] LEN:1000w
OUT:Tutorial_Markdown + Runnable_Code_Examples
"""
# Explanation: Instructor creates step-by-step tutorial with code snippets,
# screenshots, and explanations, outputs markdown with runnable code examples


# ============================================================================
# QUICK REFERENCE EXAMPLES
# ============================================================================

QUICK_REF_SIMPLE = """
ACT:Dev OBJ:Write_Code OUT:Python
"""
# Ultra-concise: "Write Python code as a developer"

QUICK_REF_MODERATE = """
ACT:Senior_Dev [Lang:Python] OBJ:Debug_Issue THINK:StepByStep OUT:Solution
"""
# Moderate: "Senior dev, debug the issue step-by-step, provide solution"

QUICK_REF_DETAILED = """
ACT:Architect [Expertise:Performance+Security] CTX:[Error_Log] OBJ:Analyze + Fix
EVAL:RootCause | Performance | Security THINK:StepByStep
OUT:Analysis + Solution + Prevention OUT:Detailed_Report
"""
# Detailed: Comprehensive analysis with multiple evaluation criteria


if __name__ == "__main__":
    prompts = {
        "code_generation": PROMPT_1_CODE_GENERATION,
        "code_review": PROMPT_2_CODE_REVIEW,
        "debugging": PROMPT_3_DEBUG_ISSUE,
        "refactoring": PROMPT_4_REFACTORING,
        "testing": PROMPT_5_TESTING,
        "api_docs": PROMPT_6_API_DOCUMENTATION,
        "readme": PROMPT_7_README_GENERATION,
        "changelog": PROMPT_8_CHANGELOG,
        "performance": PROMPT_9_PERFORMANCE_ANALYSIS,
        "security": PROMPT_10_SECURITY_AUDIT,
        "architecture": PROMPT_11_SYSTEM_DESIGN,
        "database": PROMPT_12_DATABASE_SCHEMA,
        "planning": PROMPT_13_PROJECT_PLANNING,
        "requirements": PROMPT_14_REQUIREMENTS_ANALYSIS,
        "blog": PROMPT_15_BLOG_POST,
        "marketing": PROMPT_16_MARKETING_COPY,
        "education": PROMPT_17_CONCEPT_EXPLANATION,
        "tutorial": PROMPT_18_TUTORIAL,
    }
    
    print("L-ZIP Example Prompts")
    print("=" * 70)
    for name, prompt in prompts.items():
        print(f"\n{name.upper()}:")
        print(prompt.strip())
        print("-" * 70)
