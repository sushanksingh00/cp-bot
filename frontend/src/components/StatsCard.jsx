import React from "react";

const StatsCard = ({ total_questions, total_days_active}) => {
    return (
        <div className="">
            <div className="flex gap-4 mb-4">

                <div className="w-1/2 aspect-square bg-blue-100 rounded-2xl shadow-md p-5 flex flex-col justify-center items-center">
                    <p>
                        <span className="text-xl font-semibold text-center">Total Questions:</span> 
                    </p>
                    <p className="text-5xl font-bold mt-2">
                        {total_questions}
                    </p>
                </div>

                <div className="w-1/2 aspect-square bg-blue-100 rounded-2xl shadow-md p-5 flex flex-col justify-center items-center">
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