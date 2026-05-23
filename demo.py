#!/usr/bin/env python3
"""
Data Room Reconstructor Demo
Shows the system reconstructing a founder's data room in real-time
"""

import asyncio
import sys
import os

from gemini_data_room_agents import DataRoomReconstructorService


async def demo_reconstruction():
    """Demo with realistic founder scenario"""
    print("\n" + "=" * 70)
    print("📂 Data Room Reconstruction Demo")
    print("Google I/O Hackathon 2025")
    print("=" * 70)

    # Founder scenario
    founder_email = "sarah@techstartup.io"
    company_name = "TechStartup Inc"

    print(f"\n🔍 Reconstructing data room for: {company_name}")
    print(f"Founder email: {founder_email}")
    print("\n⏳ Running 5 specialized agents in parallel...\n")
    print("  🔎 Scout Gmail Agent - Finding financial emails")
    print("  🔎 Scout Drive Agent - Discovering documents")
    print("  🔎 Scout Carta Agent - Retrieving cap table")
    print("  🔎 Scout Stripe/Ramp Agent - Getting payment data")
    print("  📂 Classifier Agent - Categorizing documents")
    print("  💰 Extractor Agent - Pulling financial metrics")
    print("  ⚠️ Gap Analyzer Agent - Identifying missing docs")
    print("  🎯 Synthesizer Agent - Creating data room view")

    try:
        service = DataRoomReconstructorService()

        result = await service.reconstruct_data_room(
            founder_email=founder_email,
            company_name=company_name,
        )

        print(f"\n✅ Reconstruction complete!\n")
        
        print("📊 SUMMARY STATISTICS:")
        print(f"  Documents found: {result['summary'].get('documents_found', 0)}")
        print(f"  Sources covered: {result['summary'].get('sources_covered', 0)}")
        print(f"  Critical gaps: {result['summary'].get('critical_gaps', 0)}")
        print(f"  Investor readiness: {result['summary'].get('investor_readiness', 0)}/100")
        print(f"  Red flags: {result['summary'].get('red_flags_count', 0)}")
        
        print(f"\n⚠️  DUE DILIGENCE RISK: {result['summary'].get('due_diligence_risk', 'unknown').upper()}")
        
        print("\n💡 KEY INSIGHTS:")
        if result['gap_analysis'].get('status') == 'success':
            gap_data = result['gap_analysis'].get('data', {})
            flags = gap_data.get('red_flags', [])
            if flags:
                print("  Red Flags Found:")
                for flag in flags[:3]:
                    if isinstance(flag, dict):
                        print(f"    - {flag.get('flag', flag)}")
                    else:
                        print(f"    - {flag}")
        
        print("\n📋 NEXT STEPS FOR FOUNDER:")
        if result['gap_analysis'].get('status') == 'success':
            gap_data = result['gap_analysis'].get('data', {})
            steps = gap_data.get('recommended_next_steps', [])
            if steps:
                for step in steps[:3]:
                    if isinstance(step, dict):
                        print(f"  • {step.get('step', step)}")
                    else:
                        print(f"  • {step}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure GOOGLE_API_KEY is set!")
        sys.exit(1)


async def main():
    """Run demo"""
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Set it with: export GOOGLE_API_KEY='your-key'")
        sys.exit(1)

    print(f"\n✅ GOOGLE_API_KEY is configured\n")

    await demo_reconstruction()

    print("\n" + "=" * 70)
    print("✅ Demo completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
