export default function LoadingSpinner() {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="relative w-12 h-12">
          {/* Outer ring */}
          <div className="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
          
          {/* Spinning ring */}
          <div className="absolute inset-0 border-4 border-transparent border-t-primary border-r-primary rounded-full animate-spin"></div>
        </div>
        <span className="ml-4 text-gray-600 font-semibold">Loading...</span>
      </div>
    );
  }