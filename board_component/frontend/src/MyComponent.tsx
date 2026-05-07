import { useEffect, useRef, useState } from "react";
import { Streamlit } from "streamlit-component-lib";

function MyComponent({ args }: any) {
  useEffect(() => {
      Streamlit.setFrameHeight();
  }, []);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const boardState = args?.board ?? Array(24).fill(" ");
  const phase = args?.phase;
  const currentPlayer = args?.current_player;
  const removable = args?.removable || []
  const ui_mode = args?.ui_mode
  const lastMove = args?.last_move;

  let from = null;
  let to = null;

  if (lastMove) {
    if (lastMove[0] === "move") {
      from = lastMove[1];
      to = lastMove[2];
    }

    if (lastMove[0] === "place" || lastMove[0] === "remove") {
      to = lastMove[1];
    }
  }

  const [selected, setSelected] = useState<number | null>(null);

  const points = [
    [25, 25], [320, 25], [615, 25],
    [140, 140], [320, 140], [500, 140],
    [255, 255], [320, 255], [385, 255],
    [25, 320], [140, 320], [255, 320], [385, 320], [500, 320], [615, 320],
    [255, 385], [320, 385], [385, 385],
    [140, 500], [320, 500], [500, 500],
    [25, 615], [320, 615], [615, 615],
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d")!;
    const r = 15;

    const draw = () => {
      ctx.clearRect(0, 0, 640, 640);

      ctx.fillStyle = "#0a1421";
      ctx.fillRect(0, 0, 640, 640);

      ctx.strokeStyle = "#d2b48c";
      ctx.lineWidth = 6;

      const pad = 25;
      const mid = 320;

      ctx.strokeRect(pad, pad, 640 - 2 * pad, 640 - 2 * pad);
      ctx.strokeRect(140, 140, 360, 360);
      ctx.strokeRect(255, 255, 130, 130);

      ctx.beginPath();
      ctx.moveTo(pad, mid);
      ctx.lineTo(640 - pad, mid);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(mid, pad);
      ctx.lineTo(mid, 640 - pad);
      ctx.stroke();

      points.forEach(([x, y], i) => {
        ctx.fillStyle = "#8b7355";
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();

        const piece = boardState[i];

        if (piece && piece !== " ") {
          if (ui_mode === "removal" && removable.includes(i)) {
              ctx.strokeStyle = "red";
              ctx.lineWidth = 4;
              ctx.beginPath();
              ctx.arc(x, y, r + 6, 0, Math.PI * 2);
              ctx.stroke();
          }
          if (selected == i) {
              ctx.strokeStyle = "green";
              ctx.lineWidth = 4;
              ctx.beginPath();
              ctx.arc(x, y, r + 6, 0, Math.PI * 2);
              ctx.stroke();
          }
          if (i === from || i === to) {
          ctx.strokeStyle = "gold";
          ctx.lineWidth = 5;
          ctx.beginPath();
          ctx.arc(x, y, r + 8, 0, Math.PI * 2);
          ctx.stroke();
          }
          ctx.fillStyle = "#f5f5f5";
          ctx.font = "bold 35px Arial";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(piece, x, y);
        }
      });
    };

    draw();
  }, [boardState, selected]);

  const handleClick = (e: any) => {
      const canvas = canvasRef.current!;
      const rect = canvas.getBoundingClientRect();

      const cx = e.clientX - rect.left;
      const cy = e.clientY - rect.top;

      let closest = -1;
      let minDist = 10000;

      points.forEach(([px, py], idx) => {
        const d = Math.hypot(px - cx, py - cy);
        if (d < 40 && d < minDist) {
          minDist = d;
          closest = idx;
        }
      });

      if (closest === -1) return;

      if (ui_mode === "removal") {
          if (removable.includes(closest)) {
            Streamlit.setComponentValue({type: "remove", pos: closest});
          }
          return;
      }

      if (phase === "placement") {
          Streamlit.setComponentValue({ type: "place", pos: closest });
          return;
      }
      
      if (selected === null) {
        if (boardState[closest] === currentPlayer) {
          setSelected(closest);
        }
      } else {
        Streamlit.setComponentValue({
          type: "move",
          from: selected,
          to: closest,
        });
        setSelected(null);
      }
    };

  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      margin: "30px 0",
      background: "#3b2b1f",
      padding: 40,
      borderRadius: 15
    }}>
      <canvas
        ref={canvasRef}
        width={640}
        height={640}
        onClick={handleClick}
        style={{
          border: "5px solid #d2b48c",
          borderRadius: 12,
          cursor: "pointer"
        }}
      />
    </div>
  );
}

export default MyComponent;