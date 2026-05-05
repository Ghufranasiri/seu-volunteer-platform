def recommend_opportunities(user, opportunities):
    recommended = []

    user_major = (user.get("major") or "").lower()
    user_interests = user.get("interests") or ""

    if isinstance(user_interests, str):
        user_interests = [
            interest.strip().lower()
            for interest in user_interests.split(",")
            if interest.strip()
        ]
    else:
        user_interests = [
            str(interest).lower()
            for interest in user_interests
            if interest
        ]

    for opp in opportunities:
        title = getattr(opp, "name", "")
        category = getattr(opp, "category", "")
        description = getattr(opp, "description", "")

        title_lower = str(title).lower()
        category_lower = str(category).lower()
        desc_lower = str(description).lower()

        score = 0

        if user_major and user_major in category_lower:
            score += 3

        if any(i in category_lower for i in user_interests):
            score += 3

        if any(i in title_lower for i in user_interests):
            score += 2

        if any(i in desc_lower for i in user_interests):
            score += 2

        if score > 0:
            recommended.append({
                "id": opp.id,
                "title": title,
                "category": category,
                "location": getattr(opp, "location", ""),
                "hours": getattr(opp, "hours", ""),
                "score": score
            })

    recommended = sorted(recommended, key=lambda x: x["score"], reverse=True)

    return recommended[:3]