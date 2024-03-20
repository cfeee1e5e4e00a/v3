export enum MeasurementType {
    TEMPERATURE = 'temp',
    HUMIDITY = 'humd',
    CURRENT = 'curr',
}

export type Measurement<T> = {
    value: T;
    timestamp: string;
};

export type MeasurementsData<T> = Array<Measurement<T>>;
