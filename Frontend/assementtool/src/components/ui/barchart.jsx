"use client"

import { TrendingUp } from "lucide-react"
import { Bar, BarChart, XAxis, YAxis } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

// Adjusted chartConfig to match levels
const chartConfig = {
  questions: {
    label: "Questions",
  },
  ANALYZING: {
    label: "Analyzing",
    color: "hsl(var(--chart-1))",
  },
  APPLYING: {
    label: "Applying",
    color: "hsl(var(--chart-2))",
  },
  CREATING: {
    label: "Creating",
    color: "hsl(var(--chart-3))",
  },
  EVALUATING: {
    label: "Evaluating",
    color: "hsl(var(--chart-4))",
  },
  REMEMBERING: {
    label: "Remembering",
    color: "hsl(var(--chart-5))",
  },
  UNDERSTANDING: {
    label: "Understanding",
    color: "hsl(var(--chart-6))",
  },
}

export function BarChartComponent({ levelCounts }) {
  // Mapping levelCounts to chart data
  const chartData = Object.entries(levelCounts).map(([level, count], index) => ({
    level,
    questions: count,
    fill: `hsl(var(--chart-${index + 1}))`, // Adjust the color dynamically
  }));

  return (
    <Card className='bg-slate-700 shadow-md p-2 rounded-lg flex flex-col justify-between h-full text-cyan-600 text-cyan-600 border-slate-900'>
      <CardHeader>
        <CardTitle>Bar Chart - Levels of Understanding</CardTitle>

      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart
            accessibilityLayer
            data={chartData}
            layout="vertical"
            margin={{ left: 0 }}
          >
            <YAxis
              dataKey="level" // Correctly matching with level data
              type="category"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={(value) =>value
              }
            />
            <XAxis dataKey="questions" type="number" hide />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Bar dataKey="questions" layout="vertical" radius={5} fill="#8884d8" />
          </BarChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col items-start gap-2 text-sm">
        <div className="leading-none text-muted-foreground">
          Showing total questions for each level of understanding
        </div>
      </CardFooter>
    </Card>
  )
}
