/**
 * Data Room Reconstructor - React UI Demo
 * Google I/O Hackathon 2025
 */

import React, { useState } from 'react';

interface DataRoomResult {
  founder_email: string;
  company_name: string;
  timestamp: string;
  data_room: {
    documents: {
      gmail_documents: any[];
      drive_documents: any[];
      carta_data: any;
      stripe_ramp_data: any;
    };
    classification: Record<string, any[]>;
    financial_metrics: Record<string, any>;
    synthesis: {
      investor_readiness_score: number;
      red_flags: any[];
      data_room_structure: any;
    };
  };
  gap_analysis: {
    critical_gaps: any[];
    due_diligence_risk: 'high' | 'medium' | 'low';
    recommended_next_steps: string[];
  };
  summary: {
    documents_found: number;
    sources_covered: number;
    critical_gaps: number;
    investor_readiness: number;
    red_flags_count: number;
    due_diligence_risk: string;
  };
}

const DataRoomReconstructorUI: React.FC = () => {
  const [founderEmail, setFounderEmail] = useState('sarah@techstartup.io');
  const [companyName, setCompanyName] = useState('TechStartup Inc');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DataRoomResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/reconstruct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ founder_email: founderEmail, company_name: companyName }),
      });

      if (!response.ok) throw new Error('Reconstruction failed');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'high':
        return '#dc2626';
      case 'medium':
        return '#f59e0b';
      case 'low':
        return '#22c55e';
      default:
        return '#6b7280';
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px', fontFamily: 'system-ui' }}>
      <h1>📂 Data Room Reconstructor</h1>
      <p>AI-powered founder data room reconstruction with Gemini 3.5 Flash</p>

      <form onSubmit={handleSubmit} style={{ marginBottom: '20px', background: '#f3f4f6', padding: '20px', borderRadius: '8px' }}>
        <div style={{ marginBottom: '12px' }}>
          <label>
            Founder Email:
            <input
              type="email"
              value={founderEmail}
              onChange={(e) => setFounderEmail(e.target.value)}
              style={{ width: '100%', padding: '8px', marginTop: '4px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>
            Company Name:
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              style={{ width: '100%', padding: '8px', marginTop: '4px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '12px 24px',
            background: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px',
            opacity: loading ? 0.5 : 1,
          }}
        >
          {loading ? '⏳ Reconstructing Data Room...' : '🚀 Reconstruct Data Room'}
        </button>
      </form>

      {error && (
        <div style={{ background: '#fee2e2', padding: '12px', borderRadius: '4px', color: '#dc2626', marginBottom: '20px' }}>
          Error: {error}
        </div>
      )}

      {result && (
        <div style={{ background: '#f9fafb', borderRadius: '8px', overflow: 'hidden' }}>
          <div style={{ background: '#1f2937', color: 'white', padding: '20px' }}>
            <h2 style={{ margin: '0 0 10px 0' }}>✅ Data Room Reconstructed</h2>
            <p style={{ margin: 0, opacity: 0.8 }}>
              {result.company_name} • {new Date(result.timestamp).toLocaleString()}
            </p>
          </div>

          {/* Summary Metrics */}
          <div style={{ padding: '20px' }}>
            <h3>📊 Summary Metrics</h3>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                gap: '12px',
                marginBottom: '20px',
              }}
            >
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', border: '1px solid #e5e7eb' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{result.summary.documents_found}</div>
                <div style={{ fontSize: '12px', color: '#666' }}>Documents Found</div>
              </div>
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', border: '1px solid #e5e7eb' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{result.summary.sources_covered}</div>
                <div style={{ fontSize: '12px', color: '#666' }}>Sources Covered</div>
              </div>
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', border: '1px solid #e5e7eb' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#3b82f6' }}>
                  {result.summary.investor_readiness}%
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>Investor Readiness</div>
              </div>
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', border: '1px solid #e5e7eb' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: getRiskColor(result.summary.due_diligence_risk) }}>
                  {result.summary.due_diligence_risk.toUpperCase()}
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>DD Risk Level</div>
              </div>
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', border: '1px solid #e5e7eb' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ef4444' }}>
                  {result.summary.red_flags_count}
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>Red Flags</div>
              </div>
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', border: '1px solid #e5e7eb' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f59e0b' }}>
                  {result.summary.critical_gaps}
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>Critical Gaps</div>
              </div>
            </div>

            {/* Data Room Structure */}
            <h3>📁 Data Room Structure</h3>
            <div style={{ background: 'white', padding: '12px', borderRadius: '4px', marginBottom: '20px', fontSize: '14px' }}>
              <div style={{ marginBottom: '8px' }}>
                <strong>📧 Email Documents:</strong> {result.data_room.documents.gmail_documents.length} found
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>📄 Drive Documents:</strong> {result.data_room.documents.drive_documents.length} found
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>📈 Cap Table Data:</strong> Available from Carta
              </div>
              <div style={{ marginBottom: '0' }}>
                <strong>💳 Payment Data:</strong> Available from Stripe/Ramp
              </div>
            </div>

            {/* Financial Metrics */}
            <h3>💰 Extracted Financial Metrics</h3>
            <div style={{ background: 'white', padding: '12px', borderRadius: '4px', marginBottom: '20px', fontSize: '14px' }}>
              {Object.entries(result.data_room.financial_metrics).map(([key, value]) => (
                <div key={key} style={{ marginBottom: '6px', display: 'flex', justifyContent: 'space-between' }}>
                  <span>{key.replace(/_/g, ' ').toUpperCase()}:</span>
                  <strong>{typeof value === 'number' ? `$${value.toLocaleString()}` : String(value)}</strong>
                </div>
              ))}
            </div>

            {/* Red Flags */}
            {result.gap_analysis.due_diligence_risk === 'high' && (
              <div style={{ background: '#fecaca', padding: '12px', borderRadius: '4px', marginBottom: '20px', borderLeft: '4px solid #dc2626' }}>
                <h3 style={{ margin: '0 0 8px 0', color: '#991b1b' }}>⚠️ HIGH DUE DILIGENCE RISK</h3>
                <p style={{ margin: 0, fontSize: '14px', color: '#7f1d1d' }}>
                  Critical gaps detected. Founder should prioritize addressing these before next investor meeting.
                </p>
              </div>
            )}

            {/* Critical Gaps */}
            {result.gap_analysis.critical_gaps.length > 0 && (
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', marginBottom: '20px', border: '1px solid #fca5a5' }}>
                <h3 style={{ margin: '0 0 8px 0', color: '#991b1b' }}>🔴 Critical Gaps Identified</h3>
                <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px' }}>
                  {result.gap_analysis.critical_gaps.slice(0, 5).map((gap: any, idx: number) => (
                    <li key={idx} style={{ marginBottom: '4px' }}>
                      {typeof gap === 'string' ? gap : gap.document || gap.name || JSON.stringify(gap)}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Next Steps */}
            {result.gap_analysis.recommended_next_steps.length > 0 && (
              <div style={{ background: 'white', padding: '12px', borderRadius: '4px', border: '1px solid #bfdbfe' }}>
                <h3 style={{ margin: '0 0 8px 0', color: '#1e40af' }}>📋 Recommended Next Steps</h3>
                <ol style={{ margin: 0, paddingLeft: '20px', fontSize: '14px' }}>
                  {result.gap_analysis.recommended_next_steps.slice(0, 5).map((step: string, idx: number) => (
                    <li key={idx} style={{ marginBottom: '4px' }}>
                      {step}
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DataRoomReconstructorUI;
