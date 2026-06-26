import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import "./DailyActivityHeapMap.css";

const DailyActivityCard = ({ dailyActivity = [] }) => {

    const endDate = new Date();

    const startDate = new Date();
    startDate.setFullYear(endDate.getFullYear() - 1);

    return (
        <div className="bg-green-100 rounded-2xl shadow-lg p-6">

            <h2 className="text-2xl font-bold mb-6">
                Daily Activity
            </h2>



            <div className="bg-white rounded-xl p-6 shadow mb-8 overflow-x-auto">

                <CalendarHeatmap
                    startDate={startDate}
                    endDate={endDate}
                    values={dailyActivity}
                    classForValue={(value) => {
                        if (!value) return "color-empty";
                        if (value.solved_count >= 4) return "color-github-4";
                        if (value.solved_count >= 3) return "color-github-3";
                        if (value.solved_count >= 2) return "color-github-2";
                        return "color-github-1";
                    }}
                />

            </div>



            <h3 className="text-xl font-semibold mb-4">
                Recent Activity
            </h3>

            <div className="space-y-3">

                {dailyActivity.map((day, index) => {

                    const successRate =
                        day.problems_attempted > 0
                            ? (
                                (day.problems_solved /
                                    day.problems_attempted) *
                                100
                            ).toFixed(1)
                            : 0;

                    return (
                        <div
                            key={index}
                            className="bg-white rounded-xl shadow p-4 flex flex-col md:flex-row md:items-center md:justify-between"
                        >

                            <div>
                                <p className="font-semibold">
                                    {day.date}
                                </p>

                                <p className="text-gray-500 text-sm">
                                    {day.problems_attempted} Attempted •{" "}
                                    {day.problems_solved} Solved
                                </p>
                            </div>

                            <div className="mt-3 md:mt-0 text-right">

                                <p className="text-lg font-bold">
                                    {successRate}%
                                </p>

                                <p className="text-gray-500 text-sm">
                                    Success Rate
                                </p>

                            </div>

                        </div>
                    );
                })}

            </div>

        </div>
    );
};

export default DailyActivityCard;