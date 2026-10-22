"""
Supply Chain Operations Research & Logistics Optimization Service
Implements Economic Order Quantity (EOQ), Reorder Point (ROP) with safety stock buffers,
Bullwhip effect variance amplification ratio, and Dijkstra shortest-path delivery routing.
Zero external library dependencies; 100% Python standard library math and heapq.
"""

import math
import heapq
from typing import Dict, Any, List, Optional, Tuple


class SupplyChainLogisticsOpsService:
    """
    Operations research service optimizing book distribution, relief logistics,
    and university supply chain inventory policies.
    """

    # Pre-modeled Bangladesh academic & relief logistics network graph
    LOGISTICS_NETWORK = {
        "Dhaka Central": [("Gazipur Hub", 30), ("Narayanganj Depot", 20), ("Manikganj Node", 65)],
        "Gazipur Hub": [("Dhaka Central", 30), ("Mymensingh Station", 85), ("Tangail Node", 60)],
        "Narayanganj Depot": [("Dhaka Central", 20), ("Cumilla Center", 80)],
        "Cumilla Center": [("Narayanganj Depot", 80), ("Feni Hub", 55), ("Chittagong Port", 130)],
        "Chittagong Port": [("Cumilla Center", 130), ("Cox's Bazar Depot", 150)],
        "Cox's Bazar Depot": [("Chittagong Port", 150)],
        "Feni Hub": [("Cumilla Center", 55)],
        "Mymensingh Station": [("Gazipur Hub", 85), ("Sylhet Division Hub", 170)],
        "Sylhet Division Hub": [("Mymensingh Station", 170)],
        "Tangail Node": [("Gazipur Hub", 60), ("Sirajganj Junction", 45)],
        "Sirajganj Junction": [("Tangail Node", 45), ("Bogura Depot", 75), ("Rajshahi University Hub", 140)],
        "Bogura Depot": [("Sirajganj Junction", 75), ("Rangpur Node", 110)],
        "Rangpur Node": [("Bogura Depot", 110)],
        "Rajshahi University Hub": [("Sirajganj Junction", 140), ("Kushtia Node", 105)],
        "Kushtia Node": [("Rajshahi University Hub", 105), ("Khulna Maritime Depot", 135)],
        "Khulna Maritime Depot": [("Kushtia Node", 135), ("Barishal River Hub", 120)],
        "Barishal River Hub": [("Khulna Maritime Depot", 120), ("Dhaka Central", 180)],
        "Manikganj Node": [("Dhaka Central", 65)]
    }

    @classmethod
    def calculate_eoq_and_rop(
        cls,
        annual_demand: float,
        order_cost_usd: float,
        holding_cost_unit_year_usd: float,
        lead_time_days: int = 7,
        demand_std_dev_daily: float = 5.0,
        service_level_pct: float = 95.0
    ) -> Dict[str, Any]:
        """
        Calculates Economic Order Quantity (EOQ), total annual inventory cost,
        safety stock, and Reorder Point (ROP).
        Guards against D <= 0, S <= 0, H <= 0, and lead_time < 0.
        """
        D = max(1.0, float(annual_demand))
        S = max(0.1, float(order_cost_usd))
        H = max(0.01, float(holding_cost_unit_year_usd))
        L = max(1, int(lead_time_days))
        sigma_d = max(0.0, float(demand_std_dev_daily))

        # EOQ Formula: sqrt((2 * D * S) / H)
        eoq = math.sqrt((2.0 * D * S) / H)
        eoq_rounded = max(1, round(eoq))

        # Annual costs
        annual_ordering_cost = (D / eoq) * S
        annual_holding_cost = (eoq / 2.0) * H
        total_inventory_cost = annual_ordering_cost + annual_holding_cost

        # Orders per year & cycle time
        orders_per_year = round(D / eoq, 2)
        cycle_time_days = round((eoq / D) * 365.0, 1)

        # Service level Z-score mapping
        if service_level_pct >= 99.0:
            z_score = 2.326
        elif service_level_pct >= 95.0:
            z_score = 1.645
        elif service_level_pct >= 90.0:
            z_score = 1.282
        else:
            z_score = 1.000

        # Safety Stock: Z * sigma_d * sqrt(L)
        daily_demand = D / 365.0
        safety_stock = z_score * sigma_d * math.sqrt(L)
        safety_stock_rounded = math.ceil(safety_stock)

        # Reorder Point (ROP) = (daily_demand * L) + safety_stock
        lead_time_demand = daily_demand * L
        rop = round(lead_time_demand + safety_stock_rounded, 1)

        return {
            "annual_demand_units": D,
            "order_cost_usd": S,
            "holding_cost_unit_year_usd": H,
            "optimal_order_quantity_eoq": eoq_rounded,
            "orders_per_year": orders_per_year,
            "cycle_time_days": cycle_time_days,
            "annual_ordering_cost_usd": round(annual_ordering_cost, 2),
            "annual_holding_cost_usd": round(annual_holding_cost, 2),
            "total_annual_inventory_cost_usd": round(total_inventory_cost, 2),
            "lead_time_days": L,
            "safety_stock_units": safety_stock_rounded,
            "reorder_point_rop_units": rop,
            "service_level_pct": service_level_pct,
            "z_score": z_score
        }

    @classmethod
    def calculate_bullwhip_effect(
        cls,
        demand_orders: List[float],
        retailer_orders: List[float]
    ) -> Dict[str, Any]:
        """
        Calculates the Bullwhip Effect ratio = Var(Orders) / Var(Demand).
        Ratio > 1.0 indicates variance amplification up the supply chain.
        """
        dem = list(demand_orders or [100, 105, 95, 110, 90, 100])
        ordr = list(retailer_orders or [100, 120, 80, 130, 70, 125])

        if len(dem) < 2 or len(ordr) < 2:
            return {
                "bullwhip_ratio": 1.0,
                "amplification_status": "NEUTRAL",
                "message": "Insufficient series points to calculate sample variance."
            }

        def variance(series: List[float]) -> float:
            mean = sum(series) / len(series)
            return sum((x - mean) ** 2 for x in series) / (len(series) - 1)

        var_dem = max(0.0001, variance(dem))
        var_ordr = max(0.0001, variance(ordr))

        ratio = round(var_ordr / var_dem, 3)

        if ratio > 1.5:
            status = "SEVERE_BULLWHIP_AMPLIFICATION"
            recommendation = "Implement VMI (Vendor-Managed Inventory) and POS data sharing to dampen upstream demand oscillation."
        elif ratio > 1.0:
            status = "MODERATE_AMPLIFICATION"
            recommendation = "Standard demand smoothing advised; coordinate order batching schedules."
        else:
            status = "DAMPENED_STABLE"
            recommendation = "Supply chain orders match end-consumer demand variance closely."

        return {
            "demand_variance": round(var_dem, 2),
            "order_variance": round(var_ordr, 2),
            "bullwhip_ratio": ratio,
            "amplification_status": status,
            "recommendation": recommendation
        }

    @classmethod
    def find_shortest_delivery_route(
        cls,
        origin_hub: str,
        destination_hub: str
    ) -> Dict[str, Any]:
        """
        Finds the shortest distance delivery route using Dijkstra's algorithm.
        """
        origin = origin_hub.strip() if origin_hub and origin_hub.strip() in cls.LOGISTICS_NETWORK else "Dhaka Central"
        dest = destination_hub.strip() if destination_hub and destination_hub.strip() in cls.LOGISTICS_NETWORK else "Chittagong Port"

        if origin == dest:
            return {
                "origin": origin,
                "destination": dest,
                "total_distance_km": 0,
                "route_path": [origin],
                "transit_hops": 0,
                "status": "IMMEDIATE_DESTINATION"
            }

        distances: Dict[str, float] = {node: float("inf") for node in cls.LOGISTICS_NETWORK}
        previous: Dict[str, Optional[str]] = {node: None for node in cls.LOGISTICS_NETWORK}
        distances[origin] = 0

        # Priority queue stores tuples of (distance, node)
        pq: List[Tuple[float, str]] = [(0.0, origin)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > distances[current_node]:
                continue

            if current_node == dest:
                break

            for neighbor, weight in cls.LOGISTICS_NETWORK.get(current_node, []):
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))

        # Reconstruct path
        path = []
        curr = dest
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

        if distances[dest] == float("inf"):
            return {
                "origin": origin,
                "destination": dest,
                "total_distance_km": -1,
                "route_path": [],
                "transit_hops": 0,
                "status": "NO_PATH_FOUND"
            }

        return {
            "origin": origin,
            "destination": dest,
            "total_distance_km": distances[dest],
            "route_path": path,
            "transit_hops": len(path) - 1,
            "status": "OPTIMAL_SHORTEST_PATH_FOUND"
        }
