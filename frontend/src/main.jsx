import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import axios from 'axios';
import './style.css';

const API='http://127.0.0.1:8000';

function App(){
  const [roles,setRoles]=useState([]);
  const [role,setRole]=useState('');
  const [file,setFile]=useState(null);
  const [session,setSession]=useState(null);
  const [question,setQuestion]=useState('');
  const [context,setContext]=useState('');
  const [answer,setAnswer]=useState('');
  const [feedback,setFeedback]=useState(null);
  const [summary,setSummary]=useState(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');

  useEffect(()=>{axios.get(`${API}/roles`).then(r=>{setRoles(r.data.roles); setRole(r.data.roles[0]||'')}).catch(()=>setError('Backend is not running. Start FastAPI first.'))},[]);

  const upload=async()=>{
    setError(''); setLoading(true);
    try{
      const fd=new FormData(); fd.append('role',role); fd.append('file',file);
      const res=await axios.post(`${API}/upload-resume`,fd);
      setSession(res.data); setQuestion(''); setSummary(null); setFeedback(null);
    }catch(e){setError(e.response?.data?.detail || 'Upload failed');}
    setLoading(false);
  }
  const gen=async()=>{
    setError(''); setLoading(true); setFeedback(null); setAnswer('');
    try{const res=await axios.post(`${API}/generate-question`,{session_id:session.session_id}); setQuestion(res.data.question); setContext(res.data.retrieved_context);}
    catch(e){setError(e.response?.data?.detail || 'Question generation failed');}
    setLoading(false);
  }
  const submit=async()=>{
    setError(''); setLoading(true);
    try{const res=await axios.post(`${API}/submit-answer`,{session_id:session.session_id,question,answer,retrieved_context:context}); setFeedback(res.data);}
    catch(e){setError(e.response?.data?.detail || 'Submit failed');}
    setLoading(false);
  }
  const getSummary=async()=>{
    setError(''); setLoading(true);
    try{const res=await axios.get(`${API}/summary/${session.session_id}`); setSummary(res.data);}
    catch(e){setError(e.response?.data?.detail || 'Summary failed');}
    setLoading(false);
  }

  return <div className="page">
    <header><h1>Role-Based Candidate Screening System</h1><p>Resume-driven RAG interview system with selectable role, vector storage, scoring, and summary.</p></header>
    {error && <div className="error">{error}</div>}
    <section className="card"><h2>1. Candidate Entry</h2><label>Select Target Role</label><select value={role} onChange={e=>setRole(e.target.value)}>{roles.map(r=><option key={r}>{r}</option>)}</select><label>Upload Resume PDF</label><input type="file" accept="application/pdf" onChange={e=>setFile(e.target.files[0])}/><button disabled={!file||!role||loading} onClick={upload}>Upload & Parse Resume</button></section>
    {session && <section className="card"><h2>2. Resume Processing</h2><p><b>Candidate:</b> {session.candidate_name}</p><p><b>Selected Role:</b> {session.role}</p><p><b>Extracted Skills:</b> {session.skills.length? session.skills.join(', '): 'No known skills detected'}</p><button onClick={gen} disabled={loading}>Generate Interview Question</button></section>}
    {question && <section className="card"><h2>3. Interactive Interview</h2><div className="question">{question}</div><details><summary>Retrieved RAG Context / Traceability</summary><pre>{context}</pre></details><textarea rows="7" value={answer} onChange={e=>setAnswer(e.target.value)} placeholder="Type candidate answer here..."></textarea><button disabled={!answer||loading} onClick={submit}>Submit Answer</button>{feedback && <div className="feedback"><b>Score:</b> {feedback.score}/10<br/><b>Feedback:</b> {feedback.feedback}<br/><button onClick={gen}>Next Question</button><button onClick={getSummary}>View Final Summary</button></div>}</section>}
    {summary && <section className="card"><h2>4. Final Summary</h2><p><b>Total Questions:</b> {summary.total_questions}</p><p><b>Average Score:</b> {summary.average_score}/10</p><p><b>Insight:</b> {summary.insight}</p>{summary.interactions.map((it,i)=><div className="qa" key={it.id}><b>Q{i+1}:</b> {it.question}<br/><b>Answer:</b> {it.answer}<br/><b>Score:</b> {it.score}/10<br/><b>Feedback:</b> {it.feedback}</div>)}</section>}
  </div>
}

createRoot(document.getElementById('root')).render(<App/>);
