import json
import sys

# JSON 파일 읽기
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 인덱스를 인자로 받아 LaTeX 문서를 생성하는 함수
def generate_latex_from_indices(start, end, output_filename):
    # 인덱스 범위에 해당하는 데이터 추출
    selected_data = data[start:end]

    content = []

    header = r'''
\documentclass{article}
\usepackage{kotex}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{scrextend}
\usepackage{setspace}
\geometry{a4paper, margin=1in}

\begin{document}

\renewcommand{\familydefault}{\sfdefault}
\onehalfspacing
'''
    content.append(header)
    
    num_pages = (len(selected_data) - 1) // 20 + 1

    for page in range(num_pages):
        content.append(r'\section*{Vocabulary List}')
        content.append(r'\begin{addmargin}[1em]{1em}')
        content.append(r'\begin{itemize}')
        for i in range(page * 20, min((page + 1) * 20, len(selected_data))):
            item = selected_data[i]
            entry = r'''
        \item \fontsize{12pt}{14pt}\selectfont \textbf{%s} - %s \newline
        The \textbf{%s} I am reading is about the future. \newline
        %s
        ''' % (item['Word'], item['Meaning'], item['Word'], item['Korean'])
            content.append(entry)
        content.append(r'\end{itemize}')
        content.append(r'\end{addmargin}')

        if page < num_pages - 1:
            content.append(r'\newpage')
    
    footer = r'\end{document}'
    content.append(footer)

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
