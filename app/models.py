# import uuid
# from datetime import datetime
# from dataclasses import dataclass, field, asdict
# from typing import List, Dict, Any

# @dataclass
# class Candidate:
#     id: str = field(default_factory=lambda: str(uuid.uuid4()))
#     name: str
#     file_path: str
#     text: str
#     score: float = 0.0
#     rank: int = 0
#     contact: Dict[str, str] = field(default_factory=dict)
#     skills: List[str] = field(default_factory=list)
#     experience: float = 0.0
#     skill_gaps: List[str] = field(default_factory=list)
#     analysis: Dict[str, Any] = field(default_factory=dict)
#     created_at: datetime = field(default_factory=datetime.utcnow)
    
#     def to_dict(self):
#         return asdict(self)
    
#     @classmethod
#     def from_dict(cls, data: dict):
#         return cls(
#             id=data.get('id', str(uuid.uuid4())),
#             name=data['name'],
#             file_path=data['file_path'],
#             text=data['text'],
#             score=data.get('score', 0.0),
#             rank=data.get('rank', 0),
#             contact=data.get('contact', {}),
#             skills=data.get('skills', []),
#             experience=data.get('experience', 0.0),
#             skill_gaps=data.get('skill_gaps', []),
#             analysis=data.get('analysis', {}),
#             created_at=data.get('created_at', datetime.utcnow())
#         )

# @dataclass
# class JobDescription:
#     id: str = field(default_factory=lambda: str(uuid.uuid4()))
#     text: str
#     required_skills: List[str] = field(default_factory=list)
#     preferred_skills: List[str] = field(default_factory=list)
#     min_experience: float = 0.0
#     created_at: datetime = field(default_factory=datetime.utcnow)
    
#     def to_dict(self):
#         return asdict(self)
    
#     @classmethod
#     def from_dict(cls, data: dict):
#         return cls(
#             id=data.get('id', str(uuid.uuid4())),
#             text=data['text'],
#             required_skills=data.get('required_skills', []),
#             preferred_skills=data.get('preferred_skills', []),
#             min_experience=data.get('min_experience', 0.0),
#             created_at=data.get('created_at', datetime.utcnow())
#         )

# @dataclass
# class RankingSession:
#     id: str = field(default_factory=lambda: str(uuid.uuid4()))
#     job_description: JobDescription
#     candidates: List[Candidate] = field(default_factory=list)
#     created_at: datetime = field(default_factory=datetime.utcnow)
#     completed_at: datetime = None
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'job_description': self.job_description.to_dict(),
#             'candidates': [c.to_dict() for c in self.candidates],
#             'created_at': self.created_at.isoformat(),
#             'completed_at': self.completed_at.isoformat() if self.completed_at else None
#         }
    
#     @classmethod
#     def from_dict(cls, data: dict):
#         return cls(
#             id=data.get('id', str(uuid.uuid4())),
#             job_description=JobDescription.from_dict(data['job_description']),
#             candidates=[Candidate.from_dict(c) for c in data['candidates']],
#             created_at=datetime.fromisoformat(data['created_at']),
#             completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None
#         )
    
#     def get_ranked_candidates(self):
#         return sorted(self.candidates, key=lambda x: x.score, reverse=True)
    
#     def get_top_candidates(self, n=5):
#         ranked = self.get_ranked_candidates()
#         return ranked[:min(n, len(ranked))]

# # Utility functions for session management
# def session_to_candidates(session_data: dict) -> List[Candidate]:
#     """Convert session data to Candidate objects"""
#     return [Candidate.from_dict(c) for c in session_data.get('rankings', [])]

# def session_to_job_description(session_data: dict) -> JobDescription:
#     """Convert session data to JobDescription object"""
#     return JobDescription(
#         text=session_data.get('job_desc', ''),
#         required_skills=session_data.get('required_skills', []),
#         min_experience=session_data.get('min_experience', 0)
#     )

# def create_ranking_session(job_desc: str, candidates: List[dict]) -> RankingSession:
#     """Create a new ranking session from raw data"""
#     job = JobDescription(text=job_desc)
#     candidate_objs = [Candidate.from_dict(c) for c in candidates]
#     return RankingSession(job_description=job, candidates=candidate_objs)