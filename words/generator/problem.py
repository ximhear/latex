import json
import random
import sys

# JSON 파일 읽기
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 인덱스를 인자로 받아 LaTeX 문서를 생성하는 함수
def generate_latex_from_indices(start, end, output_filename):
    # 인덱스 범위에 해당하는 데이터 추출
    selected_data = data[start:end]

    # 문제와 답을 랜덤하게 섞기
    random.shuffle(selected_data)
    words_list = [item["Word"] for item in selected_data]
    random.shuffle(words_list)

    content = []

    header = r'''
\documentclass{article}
\usepackage{kotex}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{scrextend}
\usepackage{setspace}
\usepackage{anyfontsize}
\geometry{a4paper, margin=1in}

\begin{document}

\renewcommand{\familydefault}{\sfdefault}
\onehalfspacing
\fontsize{12pt}{14pt}\selectfont

\section*{Vocabulary Words}
\begin{addmargin}[1em]{1em}
'''
    content.append(header)
    
    # Vocabulary Words 섹션 작성
    words_list_str = ", ".join(words_list)
    content.append(words_list_str)
    content.append(r'\end{addmargin}')

    content.append(r'\section*{Vocabulary Examples}')
    content.append(r'\begin{addmargin}[1em]{1em}')
    content.append(r'\begin{itemize}')
    
    # Vocabulary Examples 섹션 작성
    for item in selected_data:
        example = item['Example'].replace(item['Word'], "\\_\\_\\_\\_\\_\\_")
        entry = r'''
    \item %s
    \begin{quote}
    %s
    \end{quote}
''' % (example, item['Korean'])
        content.append(entry)
    
    content.append(r'\end{itemize}')
    content.append(r'\end{addmargin}')
    content.append(r'\end{document}')

    with open(output_filename, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(content))

# 명령줄 인자를 받아 시작과 끝 인덱스를 지정
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py start_index end_index output_filename")
        sys.exit(1)
    
    start_index = int(sys.argv[1])
    end_index = int(sys.argv[2])
    output_filename = sys.argv[3]

    # LaTeX 문서 생성 실행
    generate_latex_from_indices(start_index, end_index, output_filename)
