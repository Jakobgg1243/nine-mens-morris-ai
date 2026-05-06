def render_board(game):
    return f"""
    <div style="display: flex; justify-content: center; margin: 30px 0; background: #3b2b1f; padding: 40px; border-radius: 15px;">
        <canvas id="board" width="640" height="640" 
                style="border: 5px solid #d2b48c; border-radius: 12px; cursor: pointer;">
        </canvas>
    </div>

    <script>
        const canvas = document.getElementById("board");
        let boardState = {str(game.board)};
        
        const pad = 25, outer = pad, middle = pad+115, inner = pad+230, mid = 320;

        const points = {str([
            [25, 25], [320, 25], [615, 25],
            [140, 140], [320, 140], [500, 140],
            [255, 255], [320, 255], [385, 255],
            [25, 320], [140, 320], [255, 320], [385, 320], [500, 320], [615, 320],
            [255, 385], [320, 385], [385, 385],
            [140, 500], [320, 500], [500, 500],
            [25, 615], [320, 615], [615, 615],
        ])};

        function draw() {{
            const ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, 640, 640);
            ctx.fillStyle = "#0a1421";
            ctx.fillRect(0, 0, 640, 640);
            ctx.strokeStyle = "#d2b48c";
            ctx.lineWidth = 6;

            ctx.strokeRect(outer, outer, 640-2*outer, 640-2*outer);
            ctx.strokeRect(middle, middle, 640-2*middle, 640-2*middle);
            ctx.strokeRect(inner, inner, 640-2*inner, 640-2*inner);

            ctx.beginPath();
            ctx.moveTo(outer, mid); ctx.lineTo(inner, mid);
            ctx.moveTo(640-inner, mid); ctx.lineTo(640-outer, mid);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(mid, outer); ctx.lineTo(mid, inner);
            ctx.moveTo(mid, 640-inner); ctx.lineTo(mid, 640-outer);
            ctx.stroke();

            const r = 15;
            points.forEach(([x, y], i) => {{
                ctx.fillStyle = "#8b7355";
                ctx.beginPath();
                ctx.arc(x, y, r, 0, Math.PI*2);
                ctx.fill();
                
                const piece = boardState[i];
                
                if (piece && piece !== " ") {{
                    ctx.fillStyle = "#f5f5f5" ;
                    ctx.font = "bold 35px Arial";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(piece, x, y);
                }}
            }});
        }}

        canvas.addEventListener("click", (e) => {{
            const rect = canvas.getBoundingClientRect();
            const cx = e.clientX - rect.left;
            const cy = e.clientY - rect.top;

            let closest = -1;
            let minDist = 10000;

            points.forEach(([px, py], idx) => {{
                const d = Math.hypot(px - cx, py - cy);
                if (d < 40 && d < minDist) {{
                    minDist = d;
                    closest = idx;
                }}
            }});

            if (closest !== -1) {{
                console.log("Clicked position:", closest);
            }}
        }});

        draw();

        window.addEventListener("message", (e) => {{
            if (e.data && e.data.type === "update_board") {{
                boardState = e.data.board;
                draw();
            }}
        }});
    </script>
    """