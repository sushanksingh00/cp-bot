import React from "react";

const ContestStatsCard = ({ total_contests }) => {
    return (

            <div className="w-full min-h-[220px] bg-blue-100 rounded-2xl shadow-md p-5 flex flex-col justify-center items-center">
                <p className="text-xl font-semibold text-center">
                    Total Contests
                </p>

                <p className="text-5xl font-bold mt-2">
                    {total_contests}
                </p>
            </div>

    );
};

export default ContestStatsCard;