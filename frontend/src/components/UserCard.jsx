import React from "react";

const UserCard = ({ user , last_active}) => {
    
    return (
        <div className="h-full bg-blue-100 rounded-2xl shadow-md p-6 flex flex-col justify-center">
            <div className="flex flex-col lg:flex-row justify-between gap-6">
                <div>
                    <h2 className="text-4xl font-bold mb-5">
                        {user.handle}
                    </h2>

                    <p className="text-gray-600">
                        {user.rank} • {user.platform}
                    </p>

                    <p className="text-gray-500 mt-2">
                        Last Active: {last_active}
                    </p>
                </div>
               <div className="flex flex-col sm:flex-row gap-4">

                    <div className="bg-white rounded-xl p-4 text-center w-full sm:w-32 shadow">
                        <p className="text-sm text-gray-500">
                            Current
                        </p>

                        <p className="text-2xl font-bold">
                            {user.curr_rating}
                        </p>
                    </div>

                    <div className="bg-white rounded-xl p-4 text-center w-full sm:w-32 shadow">
                        <p className="text-sm text-gray-500">
                            Max
                        </p>

                        <p className="text-2xl font-bold">
                            {user.max_rating}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UserCard;