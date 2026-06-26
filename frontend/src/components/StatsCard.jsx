import React from "react";

const StatsCard = ({ total_questions, total_days_active}) => {
    return (
        <div className="">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

                <div className="w-full min-h-[180px] bg-blue-100 rounded-2xl shadow-md p-5 flex flex-col justify-center items-center">
                    <p>
                        <span className="text-xl font-semibold text-center">Total Questions:</span> 
                    </p>
                    <p className="text-5xl font-bold mt-2">
                        {total_questions}
                    </p>
                </div>

                <div className="w-full min-h-[180px] bg-blue-100 rounded-2xl shadow-md p-5 flex flex-col justify-center items-center">
                    <p>
                        <span className="text-xl font-semibold text-center">Total Active Days:</span> 
                    </p>
                    <p className="text-5xl font-bold mt-2">
                        {total_days_active}
                    </p>
                </div>
            </div>
        </div>
    );
};

export default StatsCard;