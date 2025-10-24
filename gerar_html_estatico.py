import json

# Ler o JSON
with open('municipios_regioes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Criar arquivo HTML com dados incorporados
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consulta Região de Saúde - Ministério da Saúde</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            overflow-x: hidden;
            height: 100%;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0 0 0;
            margin: 0;
            overflow-x: hidden;
            position: relative;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(168, 85, 247, 0.2) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
        }}

        .main-content {{
            flex: 1 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0 20px 40px 20px;
            position: relative;
            z-index: 1;
        }}

        .container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.2) inset;
            padding: 50px;
            max-width: 700px;
            width: 100%;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .container:hover {{
            transform: translateY(-5px);
            box-shadow: 
                0 30px 80px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.3) inset;
        }}

        h1 {{
            color: #1e293b;
            text-align: center;
            margin-bottom: 10px;
            font-size: 32px;
            font-weight: 700;
        }}

        .subtitle {{
            text-align: center;
            color: #64748b;
            margin-bottom: 30px;
            font-size: 15px;
            font-weight: 500;
        }}

        .search-box {{
            position: relative;
            margin-bottom: 20px;
        }}

        label {{
            display: block;
            margin-bottom: 8px;
            color: #1e293b;
            font-weight: 600;
            font-size: 15px;
        }}

        input[type="text"] {{
            width: 100%;
            padding: 16px 20px;
            font-size: 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            outline: none;
            transition: all 0.3s ease;
            background: white;
        }}

        input[type="text"]:focus {{
            border-color: #7e22ce;
            box-shadow: 0 0 0 4px rgba(126, 34, 206, 0.1);
            transform: translateY(-2px);
        }}

        button {{
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #1e3c72 0%, #7e22ce 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(126, 34, 206, 0.3);
        }}

        button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(126, 34, 206, 0.4);
        }}

        button:active {{
            transform: translateY(-1px);
        }}

        .result {{
            margin-top: 30px;
            padding: 25px;
            border-radius: 10px;
            display: none;
            animation: fadeIn 0.5s;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .result.success {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
        }}

        .result.error {{
            background: #ffebee;
            border-left: 4px solid #f44336;
        }}

        .result h3 {{
            color: #134074;
            margin-bottom: 15px;
            font-size: 20px;
        }}

        .result p {{
            color: #555;
            margin: 10px 0;
            line-height: 1.8;
            font-size: 15px;
        }}

        .result strong {{
            color: #134074;
        }}

        .suggestions {{
            max-height: 250px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            margin-top: 5px;
            display: none;
            background: white;
            position: absolute;
            width: 100%;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        .suggestion-item {{
            padding: 12px 18px;
            cursor: pointer;
            transition: background 0.2s;
            border-bottom: 1px solid #f5f5f5;
        }}

        .suggestion-item:last-child {{
            border-bottom: none;
        }}

        .suggestion-item:hover {{
            background: #f0f7ff;
        }}

        .suggestion-item .municipio-nome {{
            font-weight: 600;
            color: #134074;
        }}

        .suggestion-item .uf-tag {{
            display: inline-block;
            background: #0066cc;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            margin-left: 8px;
        }}

        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }}

        .page-footer {{
            background: rgba(15, 23, 42, 0.4);
            backdrop-filter: blur(20px);
            padding: 30px 20px;
            text-align: center;
            width: 100%;
            position: relative;
            left: 0;
            right: 0;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            z-index: 2;
            flex-shrink: 0;
            margin-top: auto;
        }}

        .page-footer img {{
            height: 60px;
            margin-bottom: -3px;
            margin-top: -10px;
            opacity: 0.9;
        }}

        .page-footer p {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 11px;
            line-height: 1.8;
            margin: 0;
        }}

        .info-box {{
            background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
            border-left: 4px solid #7e22ce;
            padding: 16px 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(126, 34, 206, 0.1);
        }}

        .info-box p {{
            color: #4c1d95;
            font-size: 14px;
            line-height: 1.6;
            margin: 0;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="main-content">
        <div class="container">
            <h1>🏥 Consulta Região de Saúde</h1>
        
            <div class="info-box">
                <p>📍 Digite o nome do município para descobrir sua região de saúde</p>
            </div>

            <div class="search-box">
                <label for="municipio">Nome do Município:</label>
                <input type="text" id="municipio" placeholder="Ex: São Paulo, Rio de Janeiro, Brasília..." autocomplete="off">
                <div class="suggestions" id="suggestions"></div>
        </div>

        <button onclick="buscarRegiao()">🔍 Buscar Região de Saúde</button>

        <div class="result" id="result"></div>

        <div class="footer">
            <p>Dados atualizados em Outubro de 2025</p>
        </div>
        </div>
    </div>

    <script>
        // Dados incorporados diretamente no HTML
        const municipiosData = {json.dumps(data, ensure_ascii=False)};

        console.log('Total de municípios carregados:', municipiosData.length);

        // Autocomplete
        document.getElementById('municipio').addEventListener('input', function() {{
            const input = this.value.trim().toUpperCase();
            const suggestionsDiv = document.getElementById('suggestions');
            
            if (input.length < 2) {{
                suggestionsDiv.style.display = 'none';
                return;
            }}

            const matches = municipiosData.filter(m => 
                m.NO_MUNICIPIO.includes(input)
            ).slice(0, 10);

            if (matches.length > 0) {{
                suggestionsDiv.innerHTML = matches.map(m => 
                    `<div class="suggestion-item" onclick="selecionarMunicipio('${{m.NO_MUNICIPIO}}')">
                        <span class="municipio-nome">${{m.NO_MUNICIPIO}}</span>
                        <span class="uf-tag">${{m.UF}}</span>
                    </div>`
                ).join('');
                suggestionsDiv.style.display = 'block';
            }} else {{
                suggestionsDiv.style.display = 'none';
            }}
        }});

        function selecionarMunicipio(nome) {{
            document.getElementById('municipio').value = nome;
            document.getElementById('suggestions').style.display = 'none';
            buscarRegiao();
        }}

        // Fechar suggestions ao clicar fora
        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.search-box')) {{
                document.getElementById('suggestions').style.display = 'none';
            }}
        }});

        // Buscar região ao pressionar Enter
        document.getElementById('municipio').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                buscarRegiao();
            }}
        }});

        function buscarRegiao() {{
            const input = document.getElementById('municipio').value.trim().toUpperCase();
            const resultDiv = document.getElementById('result');
            
            if (!input) {{
                alert('Por favor, digite o nome do município');
                return;
            }}

            document.getElementById('suggestions').style.display = 'none';

            const encontrados = municipiosData.filter(m => m.NO_MUNICIPIO === input);

            if (encontrados.length === 0) {{
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `
                    <h3>❌ Município não encontrado</h3>
                    <p>O município "<strong>${{input}}</strong>" não foi encontrado na base de dados.</p>
                    <p>Verifique a grafia e tente novamente.</p>
                `;
                resultDiv.style.display = 'block';
                return;
            }}

            // Agrupar por região de saúde (caso haja mais de uma)
            const regioes = [...new Set(encontrados.map(e => e.NO_REGIAO_SAUDE))];
            const uf = encontrados[0].UF;

            let html = `
                <h3>✅ Resultado da Consulta</h3>
                <p><strong>Município:</strong> ${{input}}</p>
                <p><strong>UF:</strong> ${{uf}}</p>
            `;

            if (regioes.length === 1) {{
                html += `<p><strong>Região de Saúde:</strong> ${{regioes[0]}}</p>`;
            }} else {{
                html += `<p><strong>Regiões de Saúde:</strong></p><ul>`;
                regioes.forEach(r => {{
                    html += `<li>${{r}}</li>`;
                }});
                html += `</ul>`;
            }}

            resultDiv.className = 'result success';
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
        }}
    </script>

    <footer class="page-footer">
        <img src="imgs/logo.png" alt="Ministério da Saúde">
        <p>
            Secretaria de Atenção Primária à Saúde - SAPS<br>
            Coordenação Geral de Monitoramento, Avaliação e Inteligência Analítica - CGMAIA<br>
            Ministério da Saúde 2025 - Todos os direitos reservados.
        </p>
    </footer>
</body>
</html>"""

# Salvar o arquivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Arquivo index.html criado com sucesso!')
print(f'Total de municípios incorporados: {len(data)}')
print('Agora você pode abrir o arquivo index.html diretamente no navegador.')
