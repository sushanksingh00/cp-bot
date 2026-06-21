import React from "react";

const DailyActivityCard = ({ dailyActivity = [] }) => {
    return (
        <div className="shadow-lg p-6 rounded-xl bg-green-100">
            <h2 className="text-xl font-bold mb-4">
                Daily Activity
            </h2>

            {dailyActivity.map((day, index) => (
                <div
                    key={index}
                    className="bg-white rounded-lg p-4 mb-3 shadow"
                >
                    <p>
                        <span className="font-semibold">Date:</span>{" "}
                        {day.date}
                    </p>

                    <p>
                        <span className="font-semibold">Problems Attempted:</span>{" "}
                        {day.problems_attempted}
                    </p>

                    <p>
                        <span className="font-semibold">Problems Solved:</span>{" "}
                        {day.problems_solved}
                    </p>

                    <p>
                        <span className="font-semibold">Success Rate:</span>{" "}
                        {day.problems_attempted > 0
                            ? ((day.problems_solved / day.problems_attempted) * 100).toFixed(1)
                            : 0}
                        %
                    </p>
                </div>
            ))}
        </div>
    );
};

export default DailyActivityCard;