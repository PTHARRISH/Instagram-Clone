const StatItem = ({ value, label }) => (
  <div className="text-center">
    <p className="font-semibold text-gray-900">{value}</p>
    <p className="text-sm text-gray-500">{label}</p>
  </div>
);

export default StatItem;
