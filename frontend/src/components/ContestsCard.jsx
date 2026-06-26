import React from "react";
import ContestRatingChart from "./ContestRatingChart";

const ContestsCard = ({ contests = [] }) => {

    return (
        <div className="bg-blue-100 rounded-2xl shadow-lg p-6">

            <h2 className="text-2xl font-bold mb-6">
                Contest Performance
            </h2>

            <div className="bg-white rounded-xl shadow p-6 mb-8">
                <ContestRatingChart contests={contests} />
            </div>

            <h3 className="text-xl font-semibold mb-4">
                Contest History
            </h3>

            <div className="space-y-3">

                {contests.map((contest, index) => {

                    const delta =
                        contest.new_rating - contest.old_rating;

                    return (
                        <div
                            key={index}
                            className="bg-white rounded-xl shadow p-4 flex flex-col md:flex-row md:justify-between md:items-center"
                        >

                            <div>

                                <h4 className="font-bold text-lg">
                                    {contest.contest_name}
                                </h4>

                                <p className="text-gray-500 text-sm">
                                    Rank #{contest.rank}
                                </p>

                            </div>

                            <div className="grid grid-cols-3 gap-6 mt-4 md:mt-0 text-center">

                                <div>

                                    <p className="text-lg font-bold">
                                        {contest.old_rating}
                                    </p>

                                    <p className="text-gray-500 text-sm">
                                        Old Rating
                                    </p>

                                </div>

                                <div>

                                    <p className="text-lg font-bold">
                                        {contest.new_rating}
                                    </p>

                                    <p className="text-gray-500 text-sm">
                                        New Rating
                                    </p>

                                </div>

                                <div>

                                    <p
                                        className={`text-xl font-bold ${
                                            delta >= 0
                                                ? "text-green-600"
                                                : "text-red-600"
                                        }`}
                                    >
                                        {delta >= 0 ? "+" : ""}
                                        {delta}
                                    </p>

                                    <p className="text-gray-500 text-sm">
                                        Rating Change
                                    </p>

                                </div>

                            </div>

                        </div>
                    );

                })}

            </div>

        </div>
    );
};

export default ContestsCard;