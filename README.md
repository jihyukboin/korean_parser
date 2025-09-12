파일 AWS S3 업로드  -> 
upstage.ai document parsing api 호출 후 얻은 json 파일 속에서 카테고리 , 각 페이지 별 문장 추출 -> 
openai api 호출하여 구조화 형식으로 추출 -> 
MYSQL 삽입 

파싱 프롬포트 : 

Developer message  = 
 
작업: 입력된 한국어 문장(original_text)에 대해 bilingual_sentence_blanks_classification 스키마의 JSON 객체로 빈칸 문제 생성 작업을 수행하세요. 절대 어떤 방식으로도 안내, 주석, 설명, 기타 텍스트 없이 **JSON 객체만** 출력하세요.

추가 가이드라인 및 세부 지시사항:

- output must be a **single valid JSON object** following bilingual_sentence_blanks_classification schema. No extra or surrounding text, bullet points, or comments are permitted; output must be valid JSON only.
- The "original_text" field must be **exactly byte-identical** to the input, with no normalization, correction, or modification of case, punctuation, or spacing. Take special care so that original_text matches input precisely, for similarity testing at a 100% threshold.
- For "question_template", extract as many *content words* (명사, 동사/형용사 활용형, 고유명사, 전문용어, 수량/수사, 의미 있는 영어) as possible from original_text. For each selected word (surface form only), replace its position in the sentence with a uniquely named placeholder of the form {{W01}}, {{W02}}, etc. Use ascending numbers, with as many digits as required. For words that appear multiple times, assign a distinct placeholder for each occurrence (e.g., {{W03}}, {{W04}}).
    - Non-content elements such as particles (조사), endings, pure grammatical markers, and punctuation should be left intact. If the sentence is so short that not enough blanks are possible, allow more forms, but always prioritize content words.
- **Every placeholder in question_template must have a corresponding object in the blanks array, and they must match 1:1.**
    - Each blank object requires:
        - placeholder_key: matches the placeholder in {{...}} format, unique
        - display_order: zero-based, following their order of appearance (left to right) in the template
        - grading_method: use "exact" unless semantic similarity is justified (rare)
        - answers: at least one correct, *surface-form* answer, exactly as in original_text (no synonyms/roots)
        - answer_group: for most cases use null. Only assign the same value (e.g., "G01") to multiple blanks if:
            a) they are presented as explicit enumerations with conjunctions/commas/‘와, 과, 및, 그리고, /, &’ etc, 
            b) or symmetric parallel structures (coordinate constructions). 
            - When uncertain, do NOT group.
        - (No extra fields permitted!)
- hint: Provide, in a concise Korean text, a clear rationale for (1) why each extracted word is chosen (content word principle, stopwords unselected), (2) why any blanks are grouped (or not), with evidence, and (3) explanation of display_order. State the grouping logic, especially if group labels are assigned; give the explicit reason and refer to the pattern/rule. If no groupings, state so and explain.
- Validate: Ensure that for each placeholder in question_template, there is exactly one corresponding blank in blanks, and vice versa; all placeholder_keys must exist in the template. All allowed fields must be present; do not add extra fields.

# Steps

1. Copy the exact given sentence into original_text, byte-perfect.
2. Identify and list all content words (명사, 활용형 동/형용사, 고유명사, 전문용어, 의미 있는 영어, 수량 등) in their exact surface form and sentence order.
3. Replace each occurrence of these words, in order, with a unique placeholder ({{W01}}, etc.) to form question_template.
4. For each placeholder, create a blank object as described, preserving order and using only surface forms from the original (answers).
5. Examine any possible need for grouping (answer_group) per guidance; default is null. If group is assigned, give clear pattern-based justification in hint.
6. Compose a concise Korean hint as per above guideline, referencing extracted word types, unselected stopwords, and order/grouping choices.
7. Validate all schema, matching length and order constraints.

# Output Format

- Output must be a single, valid JSON object, conforming completely to the bilingual_sentence_blanks_classification schema.
- No extraneous information, comments, markdown, or formatting; no surrounding explanation; JSON only.
- (Key order is flexible but all required keys must be present, and no additional fields).

# Examples

예시1 (순서 고정, 분리된 내용어/명사 위주 추출):

입력:  
original_text: "현재의 테이블 구조는 간단한 빈칸 퀴즈에는 적합하지만, 말씀하신 복잡한 요구사항을 처리하기에는 유연성이 부족합니다."

출력:
{
  "original_text": "현재의 테이블 구조는 간단한 빈칸 퀴즈에는 적합하지만, 말씀하신 복잡한 요구사항을 처리하기에는 유연성이 부족합니다.",
  "question_template": "{{W01}}의 {{W02}} {{W03}}는 {{W04}} {{W05}} {{W06}}에는 {{W07}}하지만, {{W08}}하신 {{W09}} {{W10}}을 {{W11}}하기에는 {{W12}}이 {{W13}}합니다.",
  "blanks": [
    {"placeholder_key": "{{W01}}","display_order":0, "grading_method":"exact", "answers":["현재"], "answer_group":null},
    {"placeholder_key": "{{W02}}","display_order":1, "grading_method":"exact", "answers":["테이블"], "answer_group":null},
    {"placeholder_key": "{{W03}}","display_order":2, "grading_method":"exact", "answers":["구조"], "answer_group":null},
    {"placeholder_key": "{{W04}}","display_order":3, "grading_method":"exact", "answers":["간단한"], "answer_group":null},
    {"placeholder_key": "{{W05}}","display_order":4, "grading_method":"exact", "answers":["빈칸"], "answer_group":null},
    {"placeholder_key": "{{W06}}","display_order":5, "grading_method":"exact", "answers":["퀴즈"], "answer_group":null},
    {"placeholder_key": "{{W07}}","display_order":6, "grading_method":"exact", "answers":["적합"], "answer_group":null},
    {"placeholder_key": "{{W08}}","display_order":7, "grading_method":"exact", "answers":["말씀"], "answer_group":null},
    {"placeholder_key": "{{W09}}","display_order":8, "grading_method":"exact", "answers":["복잡한"], "answer_group":null},
    {"placeholder_key": "{{W10}}","display_order":9, "grading_method":"exact", "answers":["요구사항"], "answer_group":null},
    {"placeholder_key": "{{W11}}","display_order":10, "grading_method":"exact", "answers":["처리"], "answer_group":null},
    {"placeholder_key": "{{W12}}","display_order":11, "grading_method":"exact", "answers":["유연성"], "answer_group":null},
    {"placeholder_key": "{{W13}}","display_order":12, "grading_method":"exact", "answers":["부족"], "answer_group":null}
  ],
  "hint": "명사, 활용형 형용사, 동사 등 내용어를 중심으로 추출하였고, 조사, 어미, 구두점 등 불용어 및 표지어는 제외하였습니다. 병렬 구조나 등위 연결된 부분이 없으므로, 모든 빈칸은 각각 순서 고정을 적용하였습니다."
}

예시2 (순서 무관 그룹 적용 예시):

입력:  
original_text: "학습, 평가, 피드백은 모두 중요합니다."

출력:
{
  "original_text": "학습, 평가, 피드백은 모두 중요합니다.",
  "question_template": "{{W01}}, {{W02}}, {{W03}}은 모두 {{W04}}합니다.",
  "blanks": [
    {"placeholder_key": "{{W01}}", "display_order":0, "grading_method":"exact", "answers":["학습"], "answer_group":"G01"},
    {"placeholder_key": "{{W02}}", "display_order":1, "grading_method":"exact", "answers":["평가"], "answer_group":"G01"},
    {"placeholder_key": "{{W03}}", "display_order":2, "grading_method":"exact", "answers":["피드백"], "answer_group":"G01"},
    {"placeholder_key": "{{W04}}", "display_order":3, "grading_method":"exact", "answers":["중요"], "answer_group":null}
  ],
  "hint": "학습, 평가, 피드백이 쉼표로 병렬 나열된 명사이므로 answer_group(G01)으로 순서 무관 그룹을 구성하였고, 그 외 내용어는 순서 고정입니다."
}

# Notes

- Placeholders **must** be present in both question_template and blanks[]. 
- Multiple occurrences of a word get unique placeholders for each position.
- Only assign answer_group when explicit, pattern-based justification per step 5(b) exists. 
- All answers must be literal surface form as in original_text.
- Hints must clearly justify all extraction and grouping choices.
- Output must be JSON only, no other text.

작업 목적, 원문 보존, content word 중심 빈칸화, 그룹 지정, 힌트 작성, 그리고 JSON ONLY - 이 단계를 엄격히 지키세요.




Prompt messages = 

다음 입력을 그대로 사용해 bilingual_sentence_blanks_classification 스키마에 맞는 JSON을 생성하세요.
절대 원문을 변형하지 마세요(공백/구두점/대소문자 유지).
문장 속 대부분의 단어(내용어 중심)를 추출하여 빈칸 문제를 만드세요.
순서 고정/순서 무관 그룹을 구분하고, 판단 근거를 hint에 서술하세요.
출력은 오직 JSON만.
입력:
{한국어+영어 문장 1개 또는 짧은 문단 1개를 여기에 그대로 붙여넣기}
옵션(있으면 사용, 없으면 빈 값 처리):
category_id: {정수 또는 비워두기}
example_where: {출처 또는 메모(선택)}
Assistant Requirements (응답 규칙)
스키마: (사용자가 제공한) bilingual_sentence_blanks_classification
필수 필드: original_text, question_template, hint, example_where, blanks
플레이스홀더: {{W01}}, {{W02}}, …(좌→우 등장 순)
각 blanks[i]는
placeholder_key = "W%02d"
display_order = i(0부터)
answer_group = null(기본) 또는 같은 정수로 묶음
grading_method = "exact"(기본)
answers = [{"answer_text": "<원문 표면형>"}] (필요 시 동일 문장 내 실제 등장 표기만 복수 허용)
Few-shot (간단 예시)
입력
현재의 테이블 구조는 간단한 빈칸 퀴즈에는 적합하지만, 말씀하신 복잡한 요구사항을 처리하기에는 유연성이 부족합니다.
올바른 출력 스케치(설명용; 실제 실행 시에는 JSON만 반환)
original_text: 위 문장을 그대로 사용.
question_template 예: {{W01}}의 {{W02}} {{W03}}는 {{W04}} {{W05}} {{W06}}에는 {{W07}}하지만, {{W08}} {{W09}} {{W10}}을 {{W11}}하기에는 {{W12}}이 {{W13}}합니다.
blanks(좌→우):
W01=현재, W02=테이블, W03=구조, W04=간단한, W05=빈칸, W06=퀴즈, W07=적합, W08=말씀하신, W09=복잡한, W10=요구사항, W11=처리, W12=유연성, W13=부족
모두 grading_method: "exact", answer_group: null
hint: “내용어 다수 추출(조사/구두점 유지). 병렬 열거 없음 → 전부 순서 고정. 표면형 그대로 정답화(예: ‘간단한’, ‘복잡한’).”



활용 예시 : 
  원문 =  '사과는 바나나이고 영어로 apple 이다. 운동의 종류는 걷기,뛰기,달리기가 있다.' 

  output_text = ' {
  "original_text": "사과는 바나나이고 영어로 apple이다. \n운동의 종류는 걷기, 뛰기 , 달리기가 있다.",
  "question_template": "{{W01}}는 {{W02}}이고 {{W03}}로 {{W04}}이다. \n{{W05}}의 {{W06}}는 {{W07}}, {{W08}} , {{W09}}가 {{W10}}.",
  "hint": "명사(사과, 바나나, 영어, 운동, 종류, 걷기, 뛰기, 달리기)와 의미 있는 영어 단어(apple), 서술 동사(있다)를 내용어로 추출했습니다. 조사는 유지(예: 는, 로, 의, 는, 가), 어미·연결어미(이고, 이다)는 문법표지로 비추출했습니다. '걷기, 뛰기 , 달리기'는 쉼표로 병렬 열거된 항목이므로 순서 무관 그룹(1)으로 묶었고, 나머지는 순서 고정(각각 null)입니다. display_order는 문장 왼쪽에서 오른쪽으로 등장하는 순서(0부터)입니다.",
  "example_where": "",
  "blanks": [
    {
      "placeholder_key": "{{W01}}",
      "display_order": 0,
      "answer_group": null,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "사과"
        }
      ]
    },
    {
      "placeholder_key": "{{W02}}",
      "display_order": 1,
      "answer_group": null,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "바나나"
        }
      ]
    },
    {
      "placeholder_key": "{{W03}}",
      "display_order": 2,
      "answer_group": null,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "영어"
        }
      ]
    },
    {
      "placeholder_key": "{{W04}}",
      "display_order": 3,
      "answer_group": null,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "apple"
        }
      ]
    },
    {
      "placeholder_key": "{{W05}}",
      "display_order": 4,
      "answer_group": null,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "운동"
        }
      ]
    },
    {
      "placeholder_key": "{{W06}}",
      "display_order": 5,
      "answer_group": null,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "종류"
        }
      ]
    },
    {
      "placeholder_key": "{{W07}}",
      "display_order": 6,
      "answer_group": 1,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "걷기"
        }
      ]
    },
    {
      "placeholder_key": "{{W08}}",
      "display_order": 7,
      "answer_group": 1,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "뛰기"
        }
      ]
    },
    {
      "placeholder_key": "{{W09}}",
      "display_order": 8,
      "answer_group": 1,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "달리기"
        }
      ]
    },
    {
      "placeholder_key": "{{W10}}",
      "display_order": 9,
      "answer_group": null,
      "grading_method": "exact",
      "answers": [
        {
          "answer_text": "있다"
        }
      ]
    }
  ]
}

'


