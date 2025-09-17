#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apex Prompt Validation Tool

이 스크립트는 apex_prompt.md에 정의된 에이펙스 프롬프트의 
품질과 효과를 검증하기 위한 도구입니다.
"""

import json
import re
from typing import Dict, List, Any, Tuple

class ApexPromptValidator:
    """에이펙스 프롬프트 출력 검증기"""
    
    def __init__(self):
        self.required_sections = [
            "서문 및 핵심 윤리 원칙",
            "거버넌스 구조 및 역할", 
            "AI 개발 수명주기(AIDC) 통합",
            "위험 평가 및 완화 프레임워크",
            "책임성 및 구제 메커니즘",
            "훈련, 인식 및 문화",
            "지속적인 모니터링, 감사 및 프레임워크 발전"
        ]
        
        self.cot_patterns = [
            "목표:",
            "근거:",
            "메커니즘:",
            "과제:"
        ]
        
        self.ethics_principles = [
            "공정성",
            "책임성", 
            "투명성",
            "보안",
            "개인정보보호",
            "무해성",
            "유익성"
        ]

    def validate_json_structure(self, response: str) -> Tuple[bool, str, Dict]:
        """JSON 구조 유효성 검증"""
        try:
            data = json.loads(response)
            
            # 루트 레벨 검증
            if 'frameworkTitle' not in data:
                return False, "Missing 'frameworkTitle' in root object", {}
            
            if 'sections' not in data:
                return False, "Missing 'sections' array in root object", {}
            
            # 섹션 구조 검증
            sections = data['sections']
            if not isinstance(sections, list):
                return False, "'sections' must be an array", {}
            
            for i, section in enumerate(sections):
                if 'sectionTitle' not in section:
                    return False, f"Section {i} missing 'sectionTitle'", {}
                
                if 'subsections' not in section:
                    return False, f"Section {i} missing 'subsections'", {}
                
                for j, subsection in enumerate(section['subsections']):
                    if 'subsectionTitle' not in subsection:
                        return False, f"Section {i}, subsection {j} missing 'subsectionTitle'", {}
                    
                    if 'content' not in subsection:
                        return False, f"Section {i}, subsection {j} missing 'content'", {}
            
            return True, "Valid JSON structure", data
            
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}", {}

    def validate_required_sections(self, data: Dict) -> Tuple[bool, List[str]]:
        """필수 섹션 존재 확인"""
        found_sections = []
        missing_sections = []
        
        sections = data.get('sections', [])
        for section in sections:
            section_title = section.get('sectionTitle', '')
            found_sections.append(section_title)
        
        for required in self.required_sections:
            if not any(required in found for found in found_sections):
                missing_sections.append(required)
        
        return len(missing_sections) == 0, missing_sections

    def validate_cot_patterns(self, data: Dict) -> Tuple[int, int]:
        """연쇄적 사고(CoT) 패턴 검증"""
        total_subsections = 0
        subsections_with_cot = 0
        
        sections = data.get('sections', [])
        for section in sections:
            subsections = section.get('subsections', [])
            for subsection in subsections:
                total_subsections += 1
                content = subsection.get('content', '')
                
                # CoT 패턴 검사
                cot_found = 0
                for pattern in self.cot_patterns:
                    if pattern in content:
                        cot_found += 1
                
                # 최소 2개 이상의 CoT 패턴이 있으면 CoT 적용된 것으로 간주
                if cot_found >= 2:
                    subsections_with_cot += 1
        
        return subsections_with_cot, total_subsections

    def validate_ethics_integration(self, data: Dict) -> Tuple[int, List[str]]:
        """윤리 원칙 통합 검증"""
        ethics_mentions = 0
        mentioned_principles = []
        
        sections = data.get('sections', [])
        for section in sections:
            subsections = section.get('subsections', [])
            for subsection in subsections:
                content = subsection.get('content', '').lower()
                
                for principle in self.ethics_principles:
                    if principle.lower() in content:
                        ethics_mentions += 1
                        if principle not in mentioned_principles:
                            mentioned_principles.append(principle)
        
        return ethics_mentions, mentioned_principles

    def check_placeholders(self, data: Dict) -> List[str]:
        """자리 표시자 텍스트 검사"""
        placeholders = [
            "[결정 예정]",
            "[세부 사항 추가 예정]", 
            "[TBD]",
            "[TODO]",
            "..."
        ]
        
        found_placeholders = []
        sections = data.get('sections', [])
        
        for section in sections:
            subsections = section.get('subsections', [])
            for subsection in subsections:
                content = subsection.get('content', '')
                
                for placeholder in placeholders:
                    if placeholder in content:
                        found_placeholders.append(f"Found '{placeholder}' in {subsection.get('subsectionTitle', 'Unknown')}")
        
        return found_placeholders

    def generate_report(self, response: str) -> str:
        """검증 보고서 생성"""
        report = []
        report.append("=== 에이펙스 프롬프트 출력 검증 보고서 ===\n")
        
        # JSON 구조 검증
        is_valid_json, json_msg, data = self.validate_json_structure(response)
        report.append(f"1. JSON 구조 검증: {'✓ PASS' if is_valid_json else '✗ FAIL'}")
        report.append(f"   {json_msg}\n")
        
        if not is_valid_json:
            return "\n".join(report)
        
        # 필수 섹션 검증
        has_all_sections, missing = self.validate_required_sections(data)
        report.append(f"2. 필수 섹션 검증: {'✓ PASS' if has_all_sections else '✗ FAIL'}")
        if missing:
            report.append(f"   누락된 섹션: {', '.join(missing)}")
        else:
            report.append(f"   모든 필수 섹션 포함 ({len(self.required_sections)}개)")
        report.append("")
        
        # CoT 패턴 검증
        cot_count, total_count = self.validate_cot_patterns(data)
        cot_percentage = (cot_count / total_count * 100) if total_count > 0 else 0
        report.append(f"3. 연쇄적 사고(CoT) 패턴 검증:")
        report.append(f"   CoT 적용된 하위 섹션: {cot_count}/{total_count} ({cot_percentage:.1f}%)")
        report.append("")
        
        # 윤리 원칙 통합 검증
        ethics_count, mentioned = self.validate_ethics_integration(data)
        report.append(f"4. 윤리 원칙 통합 검증:")
        report.append(f"   윤리 원칙 언급 횟수: {ethics_count}")
        report.append(f"   언급된 원칙: {', '.join(mentioned)}")
        report.append("")
        
        # 자리 표시자 검사
        placeholders = self.check_placeholders(data)
        report.append(f"5. 완성도 검증: {'✓ PASS' if not placeholders else '✗ FAIL'}")
        if placeholders:
            report.append(f"   발견된 자리 표시자:")
            for ph in placeholders:
                report.append(f"   - {ph}")
        else:
            report.append("   자리 표시자 없음 - 완전한 내용")
        report.append("")
        
        # 전체 평가
        total_score = 0
        max_score = 5
        
        if is_valid_json: total_score += 1
        if has_all_sections: total_score += 1
        if cot_percentage >= 70: total_score += 1
        if len(mentioned) >= 5: total_score += 1
        if not placeholders: total_score += 1
        
        report.append(f"=== 전체 평가: {total_score}/{max_score} ===")
        
        if total_score == max_score:
            report.append("🏆 EXCELLENT - 에이펙스 프롬프트 품질 기준 완전 충족")
        elif total_score >= 4:
            report.append("✨ GOOD - 대부분의 기준 충족, 소폭 개선 필요")
        else:
            report.append("⚠️ NEEDS IMPROVEMENT - 주요 기준 미충족")
        
        return "\n".join(report)


def load_sample_response() -> str:
    """샘플 응답 로드 (테스트용)"""
    return '''
{
  "frameworkTitle": "InnovateCorp 윤리적 AI 거버넌스 프레임워크",
  "sections": [
    {
      "sectionTitle": "서문 및 핵심 윤리 원칙",
      "subsections": [
        {
          "subsectionTitle": "InnovateCorp의 AI 윤리 약속",
          "content": "목표: InnovateCorp의 AI 개발 및 배포에 대한 윤리적 약속을 명확히 정의합니다. 근거: 투명성과 책임성 원칙에 따라 우리의 가치와 약속을 공개적으로 선언함으로써 사용자 신뢰를 구축합니다. 메커니즘: - 이사회 승인을 받은 AI 윤리 헌장 수립 - 연간 윤리 성과 보고서 공개 - 외부 윤리 자문위원회 운영 과제: 다양한 문화적 맥락에서의 윤리 기준 차이. 완화: 지역별 윤리 자문단 구성 및 글로컬 접근법 적용"
        }
      ]
    }
  ]
}
'''


if __name__ == "__main__":
    validator = ApexPromptValidator()
    
    # 샘플 응답으로 테스트
    sample = load_sample_response()
    report = validator.generate_report(sample)
    print(report)
    
    print("\n" + "="*50)
    print("에이펙스 프롬프트 검증 도구 준비 완료")
    print("실제 LLM 응답을 검증하려면 load_sample_response() 함수를 수정하여")
    print("실제 응답 데이터를 입력하고 다시 실행하세요.")