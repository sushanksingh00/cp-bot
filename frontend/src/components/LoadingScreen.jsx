function LoadingScreen({ text = "Loading..." }) {
    return (
        <div className="flex flex-col items-center justify-center h-[70vh]">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>

            <h2 className="mt-5 text-xl font-semibold text-gray-700">
                {text}
            </h2>

            <p className="text-gray-500 mt-1">
                Please wait...
            </p>
        </div>
    );
}

export default LoadingScreen;