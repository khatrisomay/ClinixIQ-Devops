from fastapi import APIRouter, Query, Response
from app.services.graph_generator import generate_risk_curve_svg, generate_differential_bar_svg

router = APIRouter(prefix="/api/v1/graphs", tags=["Dynamic Analytics"])

@router.get("/risk-curve", summary="Generate dynamic SVG patient risk curve")
async def get_risk_curve(condition: str = Query("Viral Upper Respiratory Infection", description="Predicted condition"), peak_day: int = Query(4, ge=1, le=12)):
    """
    Dynamically renders and streams a dark-mode vector SVG curve illustrating
    patient symptom severity trajectory versus demographic baseline.
    """
    svg_content = generate_risk_curve_svg(condition_name=condition, peak_day=peak_day)
    return Response(content=svg_content, media_type="image/svg+xml")

@router.get("/differential", summary="Generate dynamic SVG differential bar chart")
async def get_differential_chart():
    """
    Dynamically renders and streams an SVG horizontal bar chart with normalized probability matches.
    """
    svg_content = generate_differential_bar_svg()
    return Response(content=svg_content, media_type="image/svg+xml")
