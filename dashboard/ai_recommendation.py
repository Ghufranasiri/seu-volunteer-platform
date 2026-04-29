def recommend_opportunities(user, opportunities):
    recommendations = []

    for opp in opportunities:
        # Match by major
        if user.get("major") and user["major"].lower() in opp.get("category", "").lower():
            recommendations.append(opp)
            continue

        # Match by interests
        if user.get("interests"):
            for interest in user["interests"]:
                if interest.lower() in [tag.lower() for tag in opp.get("tags", [])]:
                    recommendations.append(opp)
                    break

    return recommendations
