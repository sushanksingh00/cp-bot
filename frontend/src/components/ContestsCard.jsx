import React from "react";
import ContestRatingChart from "./ContestRatingChart";

const ContestsCard = ({ contests = [] }) => {
    return (
        <div className='p-6 rounded-2xl bg-blue-100 hover:shadow-lg transition p-6 mb-4'>
            <h2 className="font-bold text-2xl pb-6">Contests</h2>
            <ContestRatingChart contests={contests}/>
            {contests.map((contest, index) => (
                <div className="bg-white p-3 mb-2 rounded-2xl hover:shadow-xl transition p-3 mb-4">
                    <div
                        key={index}
                        className="flex justify-between items-center py-2 ">
                            
                        <div>
                            <span className="font-semibold">
                                {contest.contest_name}
                            </span>
                            <span className="ml-4">
                                Rank: {contest.rank}
                            </span>
                        </div>

                        <div className="font-semibold">
                            {contest.new_rating - contest.old_rating > 0 ? "+" : ""}
                            {contest.new_rating - contest.old_rating}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ContestsCard;