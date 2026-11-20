from __future__ import annotations

from backend.runner.load import parse_stats


def test_parse_stats_extrae_metricas_agregadas(tmp_path) -> None:
    stats = tmp_path / "locust_stats.csv"
    stats.write_text(
        "Type,Name,Request Count,Failure Count,Median Response Time,Average Response Time,"
        "Min Response Time,Max Response Time,Average Content Size,Requests/s,Failures/s,"
        "50%,66%,75%,80%,90%,95%,98%,99%,99.9%,99.99%,100%\n"
        "GET,GET /casos,100,0,20,25,10,80,500,12.5,0,20,25,30,35,40,55,60,70,80,80,80\n"
        ",Aggregated,100,0,20,25,10,80,500,12.5,0,20,25,30,35,40,55,60,70,80,80,80\n",
        encoding="utf-8",
    )
    aggregate, endpoints = parse_stats(stats)
    assert aggregate["requests"] == 100
    assert aggregate["p95_ms"] == 55
    assert aggregate["error_rate"] == 0
    assert aggregate["throughput_rps"] == 12.5
    assert endpoints[0]["name"] == "GET /casos"
