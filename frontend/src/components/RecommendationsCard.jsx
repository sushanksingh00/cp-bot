import React from "react";


const RecommendationsCard = (({recommendations}) => {
    return (
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Recommendations</h2>
            {recommendations.map((rec, index) => (
                <div key={index} >
                    <p>{index}</p>
                    <p>{rec.recommendation_type} </p>
                    <p>{rec.reason} </p>
                    <p>Priority: {rec.priority_score}</p>
                </div>
            ))}
        </div>
    )
})

export default RecommendationsCard;