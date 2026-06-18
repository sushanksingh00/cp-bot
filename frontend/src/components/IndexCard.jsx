import React from 'react'

const IndexCard = ({ data }) => {
    return (
        <div className="min-w-1/3 max-w-md p-6 rounded-xl shadow-lg border bg-white">
            <h2 className="text-2xl font-bold mb-4">
                Current User
            </h2>

            <p className="mb-2">
                <span className="font-semibold">Handle:</span> {data.handle}
            </p>

            <p className="mb-2">
                <span className="font-semibold">Current Rating:</span> {data.curr_rating}
            </p>

            <p className="mb-2">
                <span className="font-semibold">Max Rating:</span> {data.max_rating}
            </p>

            <p>
                <span className="font-semibold">Rank:</span> {data.rank}
            </p>
        </div>
    )
}

export default IndexCard