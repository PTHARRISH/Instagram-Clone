const StatItem = ({ value, label }) => (
  <div className="text-center">
    <p className="text-xl font-semibold text-white">{value}</p>
    <p className="text-gray-400">{label}</p>
  </div>
);

export default StatItem;
