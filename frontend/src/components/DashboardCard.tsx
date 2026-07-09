type Props = {
    title: string;
    value: string | number;
    color?: string;
};

export default function DashboardCard({
    title,
    value,
    color = "text-slate-900",
}: Props) {
    return (
        <div className="rounded-xl bg-white p-6 shadow-sm border">
            <h3 className="text-sm text-slate-500">{title}</h3>

            <p className={`mt-3 text-3xl font-bold ${color}`}>
                {value}
            </p>
        </div>
    );
}